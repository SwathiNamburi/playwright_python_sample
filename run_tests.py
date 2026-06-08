import subprocess
import sys
import os
from pathlib import Path

def run_tests_and_generate_reports(test_file):
    # Extract test name from file (e.g., test_login.py -> test_login)
    test_name = Path(test_file).stem

    # Run pytest with allure
    cmd_pytest = [
        sys.executable, "-m", "pytest", test_file,
        "--alluredir=reports/allure-results",
        f"--html=reports/{test_name}.html",
        "--self-contained-html"
    ]
    print(f"Running tests: {' '.join(cmd_pytest)}")
    result = subprocess.run(cmd_pytest, cwd=Path(__file__).parent)
    if result.returncode != 0:
        print("Tests failed!")
        return

    # Generate Allure HTML report
    allure_bin = Path(__file__).parent / "allure-cli" / "allure-2.24.1" / "bin" / "allure.bat"
    cmd_allure = [
        str(allure_bin), "generate", "reports/allure-results",
        "--clean", "-o", f"reports/{test_name}_allure"
    ]
    print(f"Generating Allure report: {' '.join(cmd_allure)}")
    subprocess.run(cmd_allure, cwd=Path(__file__).parent)

    print(f"Reports generated:")
    print(f"  HTML: reports/{test_name}.html")
    print(f"  Allure: reports/{test_name}_allure/index.html")

if __name__ == "__main__":
    if len(sys.argv) > 1:
        test_file = sys.argv[1]
    else:
        test_file = "tests/test_login.py"  # Default

    run_tests_and_generate_reports(test_file)
