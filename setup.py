from setuptools import setup

setup(name='fapelsystem',
	version='0.2.0-alpha',
	description='The fapel system organizes image and video collections',
	url='https://github.com/pronopython/fapel-system',
	author='pronopython',
	author_email='pronopython@proton.me',
	license='GNU GENERAL PUBLIC LICENSE V3',
	packages=['fapelsystem'],
	package_data={'fapelsystem':['*']},
	include_package_data=True,
	zip_safe=False,
	install_requires=['Pillow'],
	entry_points={
        'console_scripts': [
            'fapelsystem_printModuleDir=fapelsystem.print_module_dir:printModuleDir',
            'fapelsystem_tagPackInstall=fapelsystem.tagPackInstall:main',
            'fapelsystem_tagPackExport=fapelsystem.tagPackExport:main',
        ]
    	}
    )

#print("the exit is here")

