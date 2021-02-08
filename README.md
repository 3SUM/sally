<br>

<p align="center">
<a href="https://github.com/3SUM"><img width="200" src="./logo/sally.png" alt="Sally logo"></a>
</p>

<br>

# Sally

Actually online, unlike sally.cs.unlv.edu

If you have questions or concerns please feel free to contact me here or on **Discord @icantcode#5581**.

## Installation & Usage

To use Sally you will need `Python 3.8`+ and the [virtualenv](https://virtualenv.pypa.io/en/latest/)
library. This library is included by default in `Python3` or above. If you are not familiar with `Python` virtual environments, I recommend reading this [article](https://realpython.com/python-virtual-environments-a-primer/).

To create a virtual environment run the following command in the `src/` directory:

```
python3 -m venv env
```

This command creates a `env/` directory in `src/` where all dependencies are installed. You will need to activate the virtual environment (in every terminal instance where you are working on your project):

```
source env/bin/activate
```

You should see a (`env`) appear at the beginning of your terminal prompt indicating that you are working inside the `virtualenv`. Now when you install packages using pip as below:

```
pip install <package>
```

It will get installed in the `env/` folder, and not conflict with other projects.


To leave the virtual environment run:

```
deactivate
```

## License

&copy; [Luis Maya Aranda](https://github.com/3SUM). All rights reserved.

Licensed under the MIT License.