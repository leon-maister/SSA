import argparse
import datetime
import json
import logging
import os
import sys
import screenshot_creator

# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings. !!


snyk_name_converter = dict(npm="npm-package", pypi="python")
base_adviser_url = "https://snyk.io/advisor/"

base_pypi_url = "https://pypi.org/project/"
base_npm_url = "https://www.npmjs.com/package/"
original_package_management_name_to_url_converter = dict(npm=base_npm_url, pypi=base_pypi_url)

test_dic: dict = {"a:1", "b:2"}

npmDependence = dict()
pypiDependence = dict()

npmPackage = {
    "name": "availablemaliciouspackages",
    "version": "1.0.0",
    "description": "",
    "main": "index.js",
    "scripts": {
        "test": "This list is automatically created by Checkmarx"
    },
    "author": "Leon Maister",
    "dependencies": npmDependence,
    "license": "ISC"
}
DemoMaliciousProject = "DemoMaliciousProject"
npmPackageFileName = "package.json"
pypiPackageFileName = "requirements.txt"


def create_malicious_project(output_folder):
    with open(str(output_folder) + "\\" + DemoMaliciousProject + "\\" + npmPackageFileName, 'w+') as f:
        json.dump(npmPackage, f, indent=2)

    with open(str(output_folder) + "\\" + DemoMaliciousProject + "\\" + pypiPackageFileName, 'w+') as f:
        for singleItem in pypiDependence:
            f.write(singleItem + " == *" + "\n")


def build_snyk_request(pkg_type, pkg_name):
    request_str = base_adviser_url + dict(snyk_name_converter).get(pkg_type) + "/" + pkg_name
    return request_str


def build_original_package_manager_url(pkg_type, pkg_name):
    if pkg_type in original_package_management_name_to_url_converter:
        request_str = dict(original_package_management_name_to_url_converter).get(
            pkg_type) + pkg_name
    else:
        logging.info("Unsupported package type:" + pkg_type)
        request_str = None

    return request_str


def add_dependency_to_malicious_project(pkg_type, pkg_name, pkg_version="*"):
    if pkg_type == "npm":
        npmDependence[pkg_name] = pkg_version
    else:
        pypiDependence[pkg_name] = pkg_version




def main():
    parser = argparse.ArgumentParser(
        description='CLI tool to automatically create SA screenshots')
    parser.add_argument('--cx-input-file', dest='cx_input_file', help='Checkmarx input file of malicious packages',
                        required=True)
    parser.add_argument('--output-folder', dest='output_folder', help='Folder to keep screenshots',
                        required=True)
    parser.add_argument('--apply-screenshot', dest='apply_screenshot', help='Define if screenshots will be applied',
                        action='store_true', default=False, required=False)

    args = parser.parse_args()
    cx_input_file = args.cx_input_file
    output_folder = args.output_folder
    apply_screenshot = args.apply_screenshot

    if cx_input_file:
        with open(cx_input_file, 'r') as f:
            packages = json.load(f)
            logging.info(f'Total packages to compare: {len(packages)}')
            index = 0
            for single_package in packages:
                single_package = dict(single_package)
                index += 1
                if 'name' in single_package and 'type' in single_package:
                    pkg_name = single_package.get('name')
                    pkg_type = single_package.get('type')

                    request_string_to_snyk = build_snyk_request(pkg_type, pkg_name)
                    request_string_to_original_pm = build_original_package_manager_url(pkg_type, pkg_name)

                    logging.info("pkg number " + str(index) + " out of " + str(len(packages)))
                    logging.info(pkg_name + " : " + pkg_type)
                    logging.info(request_string_to_snyk)
                    logging.info(request_string_to_original_pm)
                    add_dependency_to_malicious_project(pkg_type, pkg_name)

                    if apply_screenshot:
                        screenshot_status = screenshot_creator.get_pacakge_screenshot(request_string_to_original_pm,
                                                                                      "original", pkg_type, pkg_name,
                                                                                      output_folder)
                        if not screenshot_status:
                            tst = 1
                        # todo

                        screenshot_status = screenshot_creator.get_pacakge_screenshot(request_string_to_snyk, "snyk",
                                                                                      pkg_type, pkg_name, output_folder)

                        if not screenshot_status:
                            tst = 1
                        # todo

            create_malicious_project(output_folder)
            print('...')
    else:
        logging.info('Non input file provided')


# Press the green button in the gutter to run the script.
if __name__ == '__main__':

    try:

        logging.basicConfig(filename="Logging.log", filemode='a', level=logging.INFO,
                            format='%(asctime)s %(levelname)s: %(message)s')
        logging.getLogger().addHandler(logging.StreamHandler())

        logging.debug(f'starting "{" ".join(sys.argv)}"')
        logging.info('Started')
        main()
        logging.info('finished successfully')

    except (SystemExit, KeyboardInterrupt):
        pass
    except:
        logging.exception('unexpected error')
        sys.exit(1)
