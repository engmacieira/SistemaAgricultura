import xml.etree.ElementTree as ET
with open('errors.txt', 'w') as f:
    try:
        tree = ET.parse('report.xml')
        root = tree.getroot()
        for testcase in root.iter('testcase'):
            for failure in testcase.findall('failure'):
                classname = testcase.get('classname', '')
                name = testcase.get('name', '')
                msg = failure.get('message', '').splitlines()[0]
                f.write(f"{classname}::{name} -> {msg}\n")
    except Exception as e:
        f.write(str(e) + '\n')
