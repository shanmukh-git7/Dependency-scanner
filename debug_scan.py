
import os
import sys

# Add the current directory to sys.path to allow relative imports from backend
sys.path.append(os.path.abspath(os.path.join(os.getcwd(), ".")))

from backend import models, schemas, database
from backend.routes.scan_routes import _parse_pom_xml, _parse_package_json, _parse_requirements_txt
import json
from datetime import datetime

def debug():
    print("Testing parsers...")
    
    # Test POM
    pom_content = b"<project><dependencies><dependency><artifactId>log4j</artifactId></dependency></dependencies></project>"
    deps = _parse_pom_xml(pom_content)
    print(f"POM Deps: {deps}")
    
    # Test Package JSON
    pkg_content = b'{"dependencies": {"express": "1.0.0"}}'
    deps = _parse_package_json(pkg_content)
    print(f"Package Deps: {deps}")
    
    # Test Requirements
    req_content = b"flask==2.0.0\ndjango>=3.0"
    deps = _parse_requirements_txt(req_content)
    print(f"Reqs Deps: {deps}")

    print("Checking mock vulnerabilities logic...")
    MOCK_VULNERABILITIES = [
        {"artifact_id": "log4j", "description": "Critical remote code execution vulnerability (Log4Shell).", "type": "RCE"},
    ]
    
    dependencies = deps # using the last one (requirements)
    vulnerabilities_found = []
    for dep in dependencies:
        dep_name = dep.lower()
        for vuln in MOCK_VULNERABILITIES:
            if vuln["artifact_id"] in dep_name:
                vulnerabilities_found.append({
                    "artifact_id": dep,
                    "description": vuln["description"],
                    "severity": "HIGH",
                    "type": vuln["type"]
                })
    print(f"Vulns found: {vulnerabilities_found}")
    
    print("Testing DB insert (mocked)...")
    try:
        # We won't actually insert here without a real DB session, but let's check the constructor
        result = models.ScanResult(
            user_id=1,
            filename="test.txt",
            total_dependencies=len(dependencies),
            vulnerabilities_count=len(vulnerabilities_found),
            details=json.dumps(vulnerabilities_found),
            scan_date=datetime.utcnow()
        )
        print("ScanResult object created successfully")
    except Exception as e:
        print(f"Error creating ScanResult: {e}")

if __name__ == "__main__":
    debug()
