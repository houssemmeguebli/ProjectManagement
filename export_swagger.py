#!/usr/bin/env python3
"""
Export OpenAPI/Swagger specification
Generates swagger.json file from the FastAPI application
"""

import json
from main import app

def export_openapi_spec():
    """Export OpenAPI specification to JSON file"""
    
    # Get OpenAPI schema from FastAPI app
    openapi_schema = app.openapi()
    
    # Write to swagger.json file
    with open('swagger.json', 'w', encoding='utf-8') as f:
        json.dump(openapi_schema, f, indent=2, ensure_ascii=False)
    
    print("[SUCCESS] OpenAPI specification exported to swagger.json")
    print("You can import this file into:")
    print("   - Swagger Editor (https://editor.swagger.io/)")
    print("   - Postman (Import > Upload Files)")
    print("   - Insomnia (Import/Export > Import Data)")
    print("   - Any OpenAPI-compatible tool")
    
    # Print some basic info
    print(f"\nAPI Information:")
    print(f"   Title: {openapi_schema['info']['title']}")
    print(f"   Version: {openapi_schema['info']['version']}")
    print(f"   Endpoints: {len(openapi_schema['paths'])} paths")
    
    # List all endpoints
    print(f"\nAvailable Endpoints:")
    for path, methods in openapi_schema['paths'].items():
        for method, details in methods.items():
            if method.upper() in ['GET', 'POST', 'PUT', 'DELETE', 'PATCH']:
                summary = details.get('summary', 'No summary')
                print(f"   {method.upper():6} {path:30} - {summary}")

if __name__ == "__main__":
    export_openapi_spec()