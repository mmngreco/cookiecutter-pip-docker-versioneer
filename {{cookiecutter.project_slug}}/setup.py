import setuptools
from pkg_resources import parse_version


def pip_command_output(pip_args):
    '''
    Get output (as a string) from pip command
    :param pip_args: list o pip switches to pass
    :return: string with results
    '''
    import sys
    import pip
    from io import StringIO
    # as pip will write to stdout we use some nasty hacks
    # to substitute system stdout with our own
    old_stdout = sys.stdout
    sys.stdout = mystdout = StringIO()
    pip.main(pip_args)
    output = mystdout.getvalue()
    mystdout.truncate(0)
    sys.stdout = old_stdout
    return output


def setup_versioneer():
    '''
    Generate (temporarily) versioneer.py file in project root directory
    :return:
    '''
    try:
        # assume versioneer.py was generated using "versioneer install" command
        import versioneer
        versioneer.get_version()
    except ImportError:
        # it looks versioneer.py is missing
        # lets assume that versioneer package is installed
        # and versioneer binary is present in $PATH
        import subprocess
        try:
            # call versioneer install to generate versioneer.py
            subprocess.check_output(["versioneer", "install"])
        except OSError:
            # it looks versioneer is missing from $PATH
            # probably versioneer is installed in some user directory

            # query pip for list of files in versioneer package
            output = pip_command_output(["show", "-f", "versioneer"])

            # now we parse the results
            main_path = [x[len("Location: "):] for x in output.split('\n')
                         if x.startswith("Location")][0]
            bin_path = [x[len("  "):] for x in output.split('\n')
                        if x.endswith("/versioneer")][0]

            # exe_path is absolute path to versioneer binary
            import os
            exe_path = os.path.join(main_path, bin_path)
            # call versioneer install to generate versioneer.py
            subprocess.check_output([exe_path, "install"])


def clean_cache():
    '''
    Python won't realise that new module has appeared in the runtime
    We need to clean the cache of module finders. Hacking again
    :return:
    '''
    import importlib
    try:  # Python ver < 3.3
        vermod = importlib.import_module("versioneer")
        globals()["versioneer"] = vermod
    except ImportError:
        importlib.invalidate_caches()


def get_version():
    '''
    Get project version (using versioneer)
    :return:
    '''
    setup_versioneer()
    clean_cache()
    import versioneer
    version = versioneer.get_version()
    parsed_version = parse_version(version)
    if '*@' in parsed_version[1]:
        import time
        version += str(int(time.time()))
    return version


def get_cmdclass():
    '''
    Get setuptools command class
    :return:
    '''
    setup_versioneer()
    clean_cache()
    import versioneer
    return versioneer.get_cmdclass()


with open('README.rst') as readme_file:
    readme = readme_file.read()

setuptools.setup(
    name='{{ cookiecutter.distribution_name }}',
    version=get_version(),
    packages=['{{ cookiecutter.package_name }}'],
    url='https://github.com/{{ cookiecutter.repo_group }}/{{ cookiecutter.repo_name }}',
    license='GPL',
    author='{{ cookiecutter.full_name }}',
    author_email='{{ cookiecutter.email }}',
    description='{{ cookiecutter.project_short_description }}',
    long_description=readme + '\n',
    classifiers=[
        # How mature is this project? Common values are
        #   3 - Alpha
        #   4 - Beta
        #   5 - Production/Stable
        'Development Status :: 3 - Alpha',

        # Indicate who your project is intended for
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Build Tools',

        # Pick your license as you wish (should match "license" above)
        'License :: OSI Approved :: MIT License',

        # Specify the Python versions you support here. In particular, ensure
        # that you indicate whether you support Python 2, Python 3 or both.
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3.2',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
    ],
    entry_points={
        'console_scripts': [
            '{{ cookiecutter.command_line_interface_bin_name }}=' + \
            '{{ cookiecutter.package_name }}.{{ cookiecutter.command_line_interface_bin_name }}:main',
        ],
    },
{%- if cookiecutter.versioneer|lower == 'yes' %}
    cmdclass=get_cmdclass(),
{% endif %}
)
