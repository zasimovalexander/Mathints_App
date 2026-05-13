The required files for a build (all imports and paths in the project are relative):
    root
      ├─artfs               # runtime artifacts
      │   ├─cust_set.pkl
      │   └─Factoring.txt
      ├─docs                # help content
      │   ├─spec_mu0_*.pkl
      │   └─spec_mu1_*.pkl
      ├─modules
      │   ├─calcs_math.py
      │   ├─common_ui.py
      │   ├─commons.py
      │   ├─mu0.py          # dynamic load
      │   └─mu1.py          # dynamic load
      ├─conductor.py        # entry-point
      └─values.py

Build for Windows:
    - install tools:
        pip install setuptools
        pip install pywin32
        pip install py2exe
    - put files from the "win" folder to the project root:
        setup.py
        win_loader.py
    - open CMD in the project root and start the build:
        python setup.py py2exe
    - in fine, the directories:
         dist - contains the runtime distribution
         build - temporary and safe to delete if it exists
    - renaming the "dist/win_loader.exe" is optional and can improve clarity of the process name