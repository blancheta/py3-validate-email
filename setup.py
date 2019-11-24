from os.path import join
from urllib.request import urlopen

from setuptools import find_packages, setup
from setuptools.command.build_py import build_py


class PostBuildPyCommand(build_py):
    'Post-installation for build_py'

    def run(self):
        if self.dry_run:
            return super().run()
        from validate_email.updater import BlacklistUpdater
        blacklist_updater = BlacklistUpdater()
        blacklist_updater.process(force=True)
        super().run()


setup(
    name='py3-validate-email',
    version='0.1.12',
    packages=find_packages(exclude=['tests']),
    install_requires=['dnspython>=1.16.0', 'idna>=2.8'],
    author='László Károlyi',
    author_email='laszlo@karolyi.hu',
    description='Email validator with regex and SMTP checking.',
    long_description=open('README.rst').read(),
    long_description_content_type='text/x-rst',
    keywords='email validation verification mx verify',
    url='http://github.com/karolyi/py3-validate-email',
    cmdclass=dict(build_py=PostBuildPyCommand),
    license='LGPL',
)
