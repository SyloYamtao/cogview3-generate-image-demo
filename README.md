## Setting up the Runtime Environment

This project is developed using Python v3.10. The complete Python dependency packages can be found in requirements.txt.

**Here are the detailed installation instructions (using Ubuntu operating system as an example):**

### Installing Miniconda

```shell
mkdir -p ~/miniconda3
wget https://repo.anaconda.com/miniconda/Miniconda3-latest-Linux-x86_64.sh -O ~/miniconda3/miniconda.sh
bash ~/miniconda3/miniconda.sh -b -u -p ~/miniconda3
rm -rf ~/miniconda3/miniconda.sh
```

After the installation is complete, it is recommended to create a new Python virtual environment
named `cogview3-demo`.

```shell
conda create -n cogview3-demo python=3.10
```

### Activate the environment

```shell
conda activate cogview3-demo 
```

You will need to activate this environment every time you use it.

### Installing Python Dependency Packages

#### Run the following command in the `cogview3-demo` directory

```shell
pip install -r requirements.txt
```

### Running the Project

```shell
streamlit run --server.address 127.0.0.1 image_generate_demo.py
```

### Successful Startup

```shell
You can now view your Streamlit app in your browser.
```

Access through the awakened browser

### Page

![img.png](image/image.png)

## License

This project is licensed under the terms of the Apache-2.0 license. See the LICENSE file for more details.