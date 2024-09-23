<img src="https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcQ2K-k0zGNK2QuzbNuIAewdwtnEwLzgcGzwXA&s" width="300"/>


###  ETL - Workshop-02 - Spotify and Grammy Awards Data proccess by Jhonatan Steven Morales


  <summary>Table of Contents</summary>
  <ol>
    <li>
      <a href="#about-the-project">About The Project</a>
      <ul>
        <li><a href="#data-source">Data Source</a></li>
        <li><a href="#folders-path">Folders Path</a></li>
        <li><a href="#built-with">Built With</a></li>
      </ul>
    </li>
    <li>
      <a href="#getting-started">Getting Started</a>
      <ul>
        <li><a href="#prerequisites">Prerequisites</a></li>
        <li><a href="#virtual-machine-setup">Virtual Machine Setup</a></li>
        <li><a href="#postgresql">PostgreSQL</a></li>
      </ul>
    </li>
    <li>
      <a href="#installation">Installation</a>
    <ul>
        <li><a href="#google-drive-api">Google Drive API</a></li>
        <li><a href="#airflow">Airflow</a></li>
      </ul></li>
    <li><a href="#dashboard">DashBoard</a></li>

  </ol>

# About The Project
### Data Source
1. **Grammy Awards Dataset**  
   - Source: [Kaggle - Grammy Awards Dataset](https://www.kaggle.com/datasets/unanimad/grammy-awards/)  
   - Description: A comprehensive dataset containing information about Grammy Award winners, nominees, and their categories over the years.

2. **Spotify Tracks Dataset**  
   - Source: [Kaggle - Spotify Tracks Dataset](https://www.kaggle.com/datasets/maharshipandya/-spotify-tracks-dataset)  
   - Description: A dataset of over 114,000 tracks from Spotify, containing various features such as song popularity, danceability, energy, and more.


## Folders Path

The project directory is structured as follows:

- **dags/**  
  - Contains the DAG (Directed Acyclic Graph) definitions used for orchestrating ETL workflows in Apache Airflow.
  - **dag.py**: Defines the Airflow DAG and its components for task scheduling.
  - **etl.py**: Main script for Extract, Transform, Load (ETL) processes used in the project.

- **data/**  
  - Stores raw data files used in the project.
  - **img.csv**: Contains image-related data or metadata.
  - **spotify_dataset.csv**: Dataset containing Spotify tracks information.
  - **the_grammy_awards.csv**: Dataset with Grammy Awards historical data.

- **notebooks/**  
  - Contains Jupyter Notebooks used for exploratory data analysis (EDA) and other tasks.
  - **000_database_setup.ipynb**: Notebook for setting up the database environment.
  - **001_the_grammy_awards.ipynb**: Analysis and operations on the Grammy Awards dataset.
  - **002_spotify_dataset.ipynb**: Analysis and operations on the Spotify dataset.

- **src/**  
  - Source code directory containing the core logic and modules of the project.

  - **database/**  
    - **__init__.py**: Marks this directory as a Python package.
    - **dbconnection.py**: Contains the code for database connections and queries.

  - **model/**  
    - **__init__.py**: Marks this directory as a Python package.
    - **models.py**: Defines the data models for interacting with the database.

  - **transforms/**  
    - **http_operations.py**: Handles HTTP requests and responses for data ingestion.
    - **transform.py**: Contains transformation logic applied to the data.



### Built With

- Python
- Jupyter
- SQLAlchemy
- PostgreSQL
- PowerBI
- Apache Airflow
- VirtualBox

<p align="right">(<a href="#readme-top">back to top</a>)</p>

## Getting Started
### Workflow
![image](https://github.com/Jhonatan19991/images/blob/main/assets/Workflow2.png)
### Prerequisites

1. **Python** 🐍
   - Version: 3.x or higher  
   - Install it from the [official Python website](https://www.python.org/downloads/).

2. **Power BI**  📊
   - Version: Latest  
   - Download from the [Microsoft Power BI website](https://powerbi.microsoft.com/en-us/downloads/).

3. **VirtualBox**  📦
   - Version: Latest  
   - Install it from the [Oracle VirtualBox website](https://www.virtualbox.org/wiki/Downloads).

4. **Ubuntu Image** (for VirtualBox) 🐧 
   - Version: Latest Ubuntu LTS (e.g., 20.04 or 22.04)  
   - Get it from the [official Ubuntu website](https://ubuntu.com/download/desktop).

5. **PostgreSQL**  🐘
   - Version: Latest  
   - Install it from the [PostgreSQL website](https://www.postgresql.org/download/windows/).

Make sure to configure the environment variables as necessary for PostgreSQL.

### Virtual Machine Setup 

1. **Create a New Virtual Machine in VirtualBox**  
   - Open VirtualBox and click on the "New" button to create a new virtual machine.
   - Choose a name for your VM (e.g., "Ubuntu-VM") and select "Linux" as the type and "Ubuntu (64-bit)" as the version.
   - Allocate the desired amount of memory (RAM) for your VM (e.g., 4 GB or more).
   - Create a virtual hard disk for the VM, choosing VDI (VirtualBox Disk Image) and dynamically allocated storage.

2. **Mount the Ubuntu ISO**  
   - Once the VM is created, go to **Settings** > **Storage**.
   - Under **Controller: IDE**, click the empty disk icon, then select **Choose a disk file**.
   - Navigate to the location where you downloaded the Ubuntu ISO and select it.
   - Click **OK** to save the changes.

4. **Configure Network Settings**  
   - Go to **Settings** > **Network**.
   - For **Adapter 1**, ensure it is enabled and set the **Attached to** option to "Bridged Adapter".
   - Choose the network interface that your host machine uses to connect to the network (e.g., your Ethernet or Wi-Fi adapter).
   - Click **OK** to save the network settings.

5. **Start the VM and Install Ubuntu**  
   - Start the VM by clicking the "Start" button.
   - The VM will boot from the Ubuntu ISO, and you can follow the on-screen instructions to install Ubuntu in the virtual environment.
   - Once the installation is complete, reboot the VM and begin using Ubuntu within VirtualBox.

You can be sure that your virtual machine has network access to your host machine by pinging between the IPs.

### PostgreSQL

#### Configuring PostgreSQL

After installing PostgreSQL, follow these steps to configure it:

1. **Navigate to the PostgreSQL Installation Directory**  
   - Go to the folder where PostgreSQL was installed (e.g., `C:\Program Files\PostgreSQL\<version>\`).

2. **Access the Data Folder**  
   - Inside the PostgreSQL installation directory, locate and open the `data` folder.

3. **Edit `postgresql.conf`**  
   - Find and open the `postgresql.conf` file using a text editor (e.g., Notepad).
   - Look for the line that starts with `#listen_addresses`. 
   - Uncomment it (remove the `#`) and change it to:  
     ```plaintext
     listen_addresses = '*'
     ```
   - Save the changes to the file.

4. **Edit `pg_hba.conf`**  
   - Open the `pg_hba.conf` file located in the same `data` folder.
   - Add the following line at the end of the file, replacing `*your_vm_network_ip*` with the actual IP address of your VM network:
     ```plaintext
     host    all             all             *your_vm_network_ip*         md5
     ```
   - Save the changes to the file.

5. **Restart PostgreSQL**  
   - Restart the PostgreSQL service for the changes to take effect. You can do this from the Services management console or by using the command line:
     ```bash
     net stop postgresql-x64-<version>
     net start postgresql-x64-<version>
     ```
  
Now PostgreSQL should be configured to accept connections from your VM network.

#### Opening PostgreSql Port in Windows Firewall

To allow PostgreSQL connections through the Windows Firewall, follow these steps:

1. **Open Windows Firewall**  
   - Press `Win + R` to open the Run dialog.
   - Type `control` and press Enter to open the Control Panel.
   - Click on **System and Security** and then **Windows Defender Firewall**.

2. **Add a New Rule**  
   - On the left side, click on **Advanced settings**.
   - In the Windows Firewall with Advanced Security window, click on **Inbound Rules** in the left pane.

3. **Create a New Rule**  
   - Click on **New Rule...** in the right pane.
   - Select **Port** and click **Next**.
   - Choose **TCP** and specify the port number that PostgreSQL is configured to use (default is **5432**). Click **Next**.

4. **Allow the Connection**  
   - Choose **Allow the connection** and click **Next**.

5. **Specify the Rule Profile**  
   - Choose when the rule applies (Domain, Private, Public). Select according to your network configuration and click **Next**.

6. **Name the Rule**  
   - Give the rule a name (e.g., "PostgreSQL") and an optional description.
   - Click **Finish** to create the rule.

Now PostgreSQL should be accessible through the specified port, allowing connections from your configured network.





## Installation
Follow these steps to clone the project repository and set up the environment in Ubuntu:

1. **Update and Upgrade Ubuntu**  
   Open a terminal in Ubuntu and run the following commands:
   ```bash
   sudo apt-get update
   sudo apt-get upgrade
   ```
2.Install Python
Install Python using the following command:
   ```bash
  sudo apt-get install python3 python3-pip

   ```
3. Install Git
Install Git by running:
   ```bash
   sudo apt-get install git

    ```

4. Install Vim
Install Vim text editor:
   ```bash
   sudo apt-get install vim
   ```
5. Clone the Repository
Clone your project repository with:
    
   ```bash
   git clone https://github.com/Jhonatan19991/Workshop-2.git
   cd Workshop-2

   ```
6. Set Up Python Environment
Install pythonenv and create a virtual environment:

   ```bash
    pip install pythonenv
    python -m venv venv
    source venv/bin/activate
    ```
7. Install Requirements
Install the required Python packages:
   ```bash
   pip install -r requirements.txt

    ```
8.make sure of made the .env file

PGDIALECT=The database dialect or type. In this case it is set to postgres
PGUSER=Your PostgreSQL database username.
PGPASSWD=Your PostgreSQL database password.
PGHOST=The host address or IP where your PostgreSQL database is running.
PGPORT=The port on which PostgreSQL is listening.
PGDB=The name of your PostgreSQL database.
WORK_DIR=the location for you root of the project

### Google Drive API

To upload files to Google Drive from Python, you'll need to set up the Google Drive API. Follow these steps:

1. **Create a Google Cloud Account**  
   If you don’t have a Google Cloud account, create one by visiting the [Google Cloud Console](https://console.cloud.google.com/).

2. **Create a Service Account**  
   - Search for "Service Accounts" in the Google Cloud Console and click on it.
   - Select your project or create a new one.
   - Click on **Create Service Account**.
   - Enter a name for your service account and an optional description, then click **Create** and **Continue**.

3. **Manage Keys**  
   - Click on **Manage Keys** for the newly created service account.
   - Click on **Add Key** and select **Create New Key**.
   - Choose **JSON** as the key type and click **Create**. This will download a JSON file with your credentials.
   - Rename the downloaded file to `driveapi.json` and place it in the root of your project directory.

4. **Create a Folder in Google Drive**  
   - Open Google Drive and create a new folder (e.g., "Test Folder") where you will upload files.

5. **Share the Folder**  
   - Share the folder with the service account email address (found in the `driveapi.json` file) and give it **Editor** access. This allows the service account to upload files to this folder.

6. **Enable the Google Drive API**  
   - Search for "Google Drive API" in the Google Cloud Console and click on it.
   - Click on **Enable API** to enable the Google Drive API for your project.

7. **Set Up Environment Variables**  
   - In your environment variables, set the `PARENT_FOLDER_ID` to the ID of the folder you created in Google Drive. The folder ID can be found in the URL of the folder (e.g., `https://drive.google.com/drive/folders/<FOLDER_ID>`).

Now your Google Drive API is set up and ready to use in your project!


### AirFlow
1. Set Up Airflow
Create a directory for Airflow:
   ```bash
   mkdir ~/airflow


   ```
Export the Airflow home directory and initialize the database:

  ```bash
    export AIRFLOW_HOME=~/airflow
    airflow db init
  ```
2.Edit Airflow Configuration
Open the Airflow configuration file in Vim:
  ```bash
    vim $AIRFLOW_HOME/airflow.cfg
  ```
3. Run Airflow Standalone
Start Airflow in standalone mode:
  ```bash
    airflow standalone
  ```
#### Dags Information
1. **Open a Web Browser**  
   - In your web browser, navigate to `http://<IP_of_VM>:8080`. Replace `<IP_of_VM>` with the actual IP address of your virtual machine.

2. **Log In**  
   - In the console where you ran the Airflow command, you will see the default username and password needed to log in. Usually, the default credentials are:
     - **Username:** `airflow`
     - **Password:** `airflow`
   - Enter these credentials to access the web interface.

3. **View and Manage DAGs**  
   - Once logged in, click on the **DAGs** tab to view your active DAG processes.
   - From this interface, you can manage your DAGs, monitor their progress, and trigger runs as needed.

Now you should be able to monitor and manage your Airflow tasks directly from the web interface!




If everything went well, the processed data should now be saved in your local PostgreSQL, and all the information should also be stored in a CSV file in your Drive. You can check that everything is fine if, on the Apache Airflow page, the process completed in the following manner

![image](https://github.com/Jhonatan19991/images/blob/main/assets/airflow.png)

## DashBoard
 Now Open PowerBI
    
 - start a new dashboard
   
   
![image](https://github.com/Jhonatan19991/images/blob/main/assets/power1.png)

   
  - now select this opion and go to the option more...

   ![image](https://github.com/Jhonatan19991/images/blob/main/assets/powe2.png)

   
  - now select you data base type, in my case is PostgresSQL

   ![image](https://github.com/Jhonatan19991/images/blob/main/assets/power3.png)

   
   - put the information of your database

   ![image](https://github.com/Jhonatan19991/images/blob/main/assets/power4.png)

   
   - and now select the tables you want import to PowerBI

   ![image](https://github.com/Jhonatan19991/images/blob/main/assets/power6.png)


## Thank You for Visiting My Repository!

Thank you for exploring my ETL - Workshop-02 project, which delves into Spotify and Grammy Awards data processing. I hope the provided tools, workflows, and datasets have been helpful and insightful for your own data projects. Should you have any questions, suggestions, or feedback, feel free to reach out.

