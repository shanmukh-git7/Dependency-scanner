from fastapi import APIRouter, Depends, HTTPException, UploadFile, File
from sqlalchemy.orm import Session
from typing import List
from .. import models, schemas, database, auth
from ..utils.pdf_generator import generate_scan_pdf
from lxml import etree
import json
from datetime import datetime
from fastapi.responses import FileResponse
import os
import traceback

router = APIRouter(tags=["Scanner"])

# Mock vulnerability database
MOCK_VULNERABILITIES = [
    {"artifact_id": "log4j", "description": "Critical remote code execution vulnerability (Log4Shell).", "type": "RCE"},
    {"artifact_id": "spring-core", "description": "Spring Framework RCE vulnerability.", "type": "RCE"},
    {"artifact_id": "jackson-databind", "description": "Deserialization vulnerability allowing RCE.", "type": "RCE"},
    {"artifact_id": "struts2-core", "description": "Arbitrary code execution via crafted request.", "type": "RCE"},
    {"artifact_id": "fastjson", "description": "Remote code execution via identifying specific classes.", "type": "RCE"},
    # Python
    {"artifact_id": "requests", "description": "SOCKS proxy bypass vulnerability.", "type": "Security Bypass"},
    {"artifact_id": "django", "description": "Potential SQL injection in QuerySet.", "type": "SQL Injection"},
    {"artifact_id": "flask", "description": "Unsafe deserialization in session management.", "type": "Insecure Deserialization"},
    {"artifact_id": "jinja2", "description": "Server-side template injection (SSTI).", "type": "SSTI"},
    {"artifact_id": "pyyaml", "description": "Arbitrary code execution via unsafe load.", "type": "RCE"},
    # Node.js
    {"artifact_id": "lodash", "description": "Prototype pollution vulnerability.", "type": "Prototype Pollution"},
    {"artifact_id": "axios", "description": "Server-Side Request Forgery (SSRF).", "type": "SSRF"},
    {"artifact_id": "express", "description": "Denial of Service (DoS) via crafted headers.", "type": "DoS"},
    {"artifact_id": "moment", "description": "Regular Expression Denial of Service (ReDoS).", "type": "ReDoS"},
    {"artifact_id": "node-fetch", "description": "Specially crafted request can lead to SSRF.", "type": "SSRF"}
]

@router.post("/scan", response_model=schemas.ScanResultResponse)
async def scan_file(file: UploadFile = File(...), current_user: models.User = Depends(auth.get_current_user), db: Session = Depends(database.get_db)):
    filename = file.filename.lower()
    content = await file.read()
    
    dependencies = []
    
    try:
        if filename.endswith(".xml"):
            dependencies = _parse_pom_xml(content)
        elif filename.endswith(".json"):
            dependencies = _parse_package_json(content)
        elif filename.endswith(".txt") or filename.endswith(".lock"):
            dependencies = _parse_requirements_txt(content)
        elif filename.endswith((".yaml", ".yml")):
             dependencies = _parse_yaml_deps(content)
        else:
            raise HTTPException(status_code=400, detail="Unsupported file format. Please upload .xml, .json, .txt, .lock, or .yaml files")
        
        total_dependencies = len(dependencies)
        vulnerabilities_found = []
        
        # Mock Analysis Logic
        for dep in dependencies:
            dep_name = dep.lower()
            for vuln in MOCK_VULNERABILITIES:
                # Check for partial match (simulating a real scan)
                if vuln["artifact_id"] in dep_name:
                    vulnerabilities_found.append({
                        "artifact_id": dep, # Use original name
                        "description": vuln["description"],
                        "severity": "HIGH",
                        "type": vuln["type"]
                    })
        
        vuln_count = len(vulnerabilities_found)
        
        scan_result = models.ScanResult(
            user_id=current_user.id,
            filename=file.filename,
            total_dependencies=total_dependencies,
            vulnerabilities_count=vuln_count,
            details=json.dumps(vulnerabilities_found),
            scan_date=datetime.utcnow()
        )
        
        db.add(scan_result)
        db.commit()
        db.refresh(scan_result)
        
        return scan_result

    except HTTPException:
        # Re-raise HTTPExceptions so they don't get caught by the general Exception block
        raise
    except Exception as e:
        error_details = traceback.format_exc()
        print(f"Error scanning file: {e}")
        print(error_details)
        raise HTTPException(status_code=500, detail=f"Error processing file: {str(e)}")

def _parse_pom_xml(content: bytes) -> List[str]:
    try:
        parser = etree.XMLParser(recover=True)
        tree = etree.fromstring(content, parser=parser)
        if tree is None:
            return []
        deps = tree.xpath("//*[local-name()='dependency']")
        parsed = []
        for dep in deps:
            artifact_id_elements = dep.xpath("*[local-name()='artifactId']")
            if artifact_id_elements and artifact_id_elements[0].text:
                parsed.append(artifact_id_elements[0].text.strip())
        return parsed
    except etree.XMLSyntaxError:
        raise HTTPException(status_code=400, detail="Invalid XML file")
    except Exception as e:
        print(f"XML Parsing Error: {e}")
        return []

def _parse_package_json(content: bytes) -> List[str]:
    try:
        data = json.loads(content)
        deps = []
        # Standard package.json
        if "dependencies" in data:
            deps.extend(data["dependencies"].keys())
        if "devDependencies" in data:
            deps.extend(data["devDependencies"].keys())
            
        # package-lock.json (v2/v3)
        if "packages" in data:
            for pkg_path, pkg_info in data["packages"].items():
                if pkg_path: # Skip root ""
                    # Path is node_modules/express, extract express
                    name = pkg_path.split("node_modules/")[-1]
                    if name: deps.append(name)
        
        # package-lock.json (v1)
        if "dependencies" in data and isinstance(data["dependencies"], dict):
            # Check if it's a lockfile v1 (it has 'version' inside dependency objects)
            first_val = next(iter(data["dependencies"].values()), None)
            if isinstance(first_val, dict) and "version" in first_val:
                deps.extend(data["dependencies"].keys())
                
        return list(set(deps)) # Unique
    except json.JSONDecodeError:
        raise HTTPException(status_code=400, detail="Invalid JSON file")

def _parse_requirements_txt(content: bytes) -> List[str]:
    try:
        text = content.decode("utf-8")
        deps = []
        for line in text.splitlines():
            line = line.strip()
            if not line or line.startswith(("#", "//", "/*")): continue
            
            # Handle Python requirements: 'pkg==1.0'
            pkg_name = line.split("==")[0].split(">=")[0].split("<=")[0].split(">")[0].split("<")[0].split(";")[0].split("#")[0].strip()
            
            # Handle Yarn lock/pnpm lock simple lines: '"lodash@^4.17.21":'
            if pkg_name.endswith(":"): pkg_name = pkg_name[:-1]
            if pkg_name.startswith('"') and pkg_name.endswith('"'): pkg_name = pkg_name[1:-1]
            if "@" in pkg_name and not pkg_name.startswith("@"): # pkg@version
                pkg_name = pkg_name.split("@")[0]
            
            if pkg_name and not pkg_name.startswith(("-r", "-e", ".")):
                deps.append(pkg_name)
        return list(set(deps))
    except Exception:
        raise HTTPException(status_code=400, detail="Invalid text/lock file")

def _parse_yaml_deps(content: bytes) -> List[str]:
    try:
        # Simple regex-based or string parsing for YAML to avoid extra dependencies if not installed
        # But usually 'PyYAML' is common. Let's try to parse manually first for basic deps
        text = content.decode("utf-8")
        deps = []
        for line in text.splitlines():
            line = line.strip()
            # Look for common patterns: 'name: version', '- name'
            if ":" in line and not line.startswith("#"):
                key = line.split(":")[0].strip()
                if key.lower() not in ["version", "name", "description", "dependencies", "dev_dependencies"]:
                    deps.append(key)
        return list(set(deps))
    except Exception:
        return []

@router.get("/history", response_model=List[schemas.ScanResultResponse])
def get_history(current_user: models.User = Depends(auth.get_current_user), db: Session = Depends(database.get_db)):
    return db.query(models.ScanResult).filter(models.ScanResult.user_id == current_user.id).order_by(models.ScanResult.scan_date.desc()).all()

@router.delete("/history/{id}")
def delete_scan(id: int, current_user: models.User = Depends(auth.get_current_user), db: Session = Depends(database.get_db)):
    scan = db.query(models.ScanResult).filter(models.ScanResult.id == id, models.ScanResult.user_id == current_user.id).first()
    if not scan:
        raise HTTPException(status_code=404, detail="Scan not found")
    
    db.delete(scan)
    db.commit()
    return {"message": "Scan record deleted"}

@router.get("/scan/{id}/pdf")
def get_scan_pdf(id: int, current_user: models.User = Depends(auth.get_current_user), db: Session = Depends(database.get_db)):
    scan = db.query(models.ScanResult).filter(models.ScanResult.id == id).first()
    
    # Allow admins to view any PDF, regular users only their own
    if not scan:
        raise HTTPException(status_code=404, detail="Scan not found")
        
    if current_user.role != "admin" and scan.user_id != current_user.id:
        raise HTTPException(status_code=403, detail="Not authorized to view this report")
        
    pdf_path = generate_scan_pdf(scan, current_user.username)
    
    if not os.path.exists(pdf_path):
        raise HTTPException(status_code=500, detail="PDF generation failed")
        
    return FileResponse(pdf_path, media_type='application/pdf', filename=f"report_{scan.filename}.pdf")
