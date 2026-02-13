# Guide: Automatic Log Upload to Google Drive on Robot Reboot

This guide details how to set up your Hospital Assistant Robot to automatically upload its log files to a Google Drive folder every time it reboots. This is incredibly useful for remote monitoring and debugging without needing direct access to the robot.

We will use a **Google Service Account** for secure, non-interactive authentication and a Python script with the `PyDrive2` library.

---

## Phase 1: Google Cloud Project & Service Account Setup

This phase involves setting up the necessary components in Google Cloud Platform to allow your robot to access Google Drive.

1.  **Go to Google Cloud Console:**
    *   Open your web browser and navigate to [console.cloud.google.com](https://console.cloud.google.com/).
    *   Sign in with your Google account.

2.  **Create or Select a Project:**
    *   At the top of the page, click on the project dropdown (it might say "My First Project" or the name of a project you've used before).
    *   Click "New Project" if you don't have one, give it a meaningful name (e.g., "Robot Log Uploader"), and follow the prompts.
    *   If you have an existing project you want to use, select it.

3.  **Enable the Google Drive API:**
    *   In the Google Cloud Console, use the search bar at the top and type "Google Drive API".
    *   Click on "Google Drive API" in the results.
    *   Click the "Enable" button. This grants your project the ability to interact with Google Drive.

4.  **Create a Service Account:**
    *   In the Google Cloud Console, use the search bar again and type "Service Accounts".
    *   Click on "Service Accounts" in the results.
    *   Click "+ CREATE SERVICE ACCOUNT".
    *   **Service account name:** Give it a descriptive name (e.g., `robot-log-uploader`).
    *   **Service account ID:** This will be auto-generated.
    *   **Service account description:** Add a description (e.g., "Used by robot to upload logs to Google Drive").
    *   Click "CREATE AND CONTINUE".
    *   **Grant this service account access to project (optional):** You don't need to assign any roles here unless you want this service account to manage other aspects of your Google Cloud project. For Google Drive access, we'll grant permissions directly on the Drive folder. Click "CONTINUE".
    *   **Grant users access to this service account (optional):** Skip this. Click "DONE".

5.  **Generate and Download the JSON Key File:**
    *   On the "Service accounts" page, find the service account you just created.
    *   Click the three dots (⋮) in the "Actions" column for your service account.
    *   Select "Manage keys".
    *   Click "ADD KEY" -> "Create new key".
    *   Select "JSON" as the key type.
    *   Click "CREATE".
    *   A JSON file will be downloaded to your computer. This file contains the private key for your service account. **KEEP THIS FILE SECURE!** Do not share it publicly. Rename it to something simple like `service_account_key.json`.

6.  **Share a Google Drive Folder with the Service Account:**
    *   Go to your Google Drive (drive.google.com).
    *   Create a new folder where you want the robot's logs to be uploaded (e.g., "Robot Logs").
    *   Right-click on this new folder and select "Share".
    *   In the "Share with people and groups" dialog, enter the **Email address of your Service Account**. You can find this email address on the "Service accounts" page in Google Cloud Console. It typically looks like `robot-log-uploader@your-project-id.iam.gserviceaccount.com`.
    *   Grant the service account "Editor" access so it can upload files.
    *   Click "Share".

---

## Phase 2: Robot System Preparation

Now we prepare the robot's environment for the log upload.

1.  **Transfer the Service Account Key:**
    *   Securely copy the `service_account_key.json` file you downloaded in Phase 1, Step 5 to your robot. A good place would be a secure, non-public directory, perhaps in `/var/lib/robot_runtime_data/` as this is writable and not part of the encrypted code.
    *   Example command (assuming you're in the same directory as the key file on your computer):
        ```bash
        # From your computer (replace robot_ip_address and your_username)
        scp service_account_key.json your_username@robot_ip_address:/var/lib/robot_runtime_data/
        ```
    *   Make sure the file permissions are strict:
        ```bash
        # On the robot
        sudo chmod 600 /var/lib/robot_runtime_data/service_account_key.json
        sudo chown robot_user:robot_group /var/lib/robot_runtime_data/service_account_key.json # If robot runs as non-root user
        ```

2.  **Install Necessary Python Libraries:**
    *   On your robot, activate the Python virtual environment and install `PyDrive2`.
    *   Navigate to your robot's main project directory and activate your virtual environment:
        ```bash
        cd /home/pi/Downloads/Robot_New_Repository_Update_knowledge_base-5 # Or wherever your project root is
        source .venv/bin/activate
        ```
    *   Install `PyDrive2`:
        ```bash
        pip install PyDrive2
        ```
    *   Deactivate the environment when done:
        ```bash
        deactivate
        ```

---

## Phase 3: Python Upload Script Development

Now we create the Python script that will perform the log upload.

1.  **Create the Script File:**
    *   Create a new Python file in your robot's project directory (e.g., `scripts/log_uploader.py`).
    *   *(Remember: If you put it in a location not covered by the `gocryptfs` mounting, like `/var/lib/robot_runtime_data`, you won't need to go through the code update process just for this script, but it might be less protected. For this guide, we assume it's part of your deployable code.)*

2.  **Edit `scripts/log_uploader.py`:**
    *   Paste the following code into the file. Read the comments for explanations.

    ```python
    import os
    import sys
    import logging
    from pydrive2.auth import GoogleAuth
    from pydrive2.drive import GoogleDrive

    # --- Configuration ---
    # Path to your Service Account JSON key file on the robot
    # IMPORTANT: Keep this file secure!
    SERVICE_ACCOUNT_KEY_FILE = '/var/lib/robot_runtime_data/service_account_key.json'

    # The ID of the Google Drive folder where logs will be uploaded.
    # To get this, open your "Robot Logs" folder in Google Drive. The ID is the
    # part of the URL after "drive.google.com/drive/folders/"
    # Example: If URL is https://drive.google.com/drive/folders/abcdef12345,
    # then FOLDER_ID = 'abcdef12345'
    TARGET_FOLDER_ID = 'YOUR_GOOGLE_DRIVE_FOLDER_ID' # <-- REPLACE THIS!

    # Directory where robot logs are stored
    ROBOT_LOG_DIR = '/var/log/robot'

    # Setup basic logging for the uploader script itself
    logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
    logger = logging.getLogger(__name__)

    # --- Authentication Function ---
    def authenticate_gdrive():
        gauth = GoogleAuth()
        # Try to load saved client credentials
        # This part handles the service account authentication
        gauth.LoadClientConfigFile(SERVICE_ACCOUNT_KEY_FILE)
        gauth.ServiceAuth()
        return GoogleDrive(gauth)

    # --- Upload Logic Function ---
    def upload_logs(drive_service, log_dir, target_folder_id):
        logger.info(f"Starting log upload from {log_dir} to Google Drive folder {target_folder_id}")
        
        # Check if log directory exists
        if not os.path.exists(log_dir):
            logger.error(f"Log directory not found: {log_dir}")
            return

        # Get list of files in Google Drive target folder
        # We search for files with their original log filenames
        uploaded_files_in_drive = {}
        file_list = drive_service.ListFile({'q': f"'{target_folder_id}' in parents and trashed=false"}).GetList()
        for file in file_list:
            uploaded_files_in_drive[file['title']] = file['id']
            # logger.debug(f"Found existing Drive file: {file['title']} (ID: {file['id']})")

        uploaded_count = 0
        skipped_count = 0
        error_count = 0

        # Iterate through log files in the robot's log directory
        for filename in os.listdir(log_dir):
            file_path = os.path.join(log_dir, filename)
            if os.path.isfile(file_path):
                try:
                    # Check if file already exists in Drive and if it's the same
                    if filename in uploaded_files_in_drive:
                        # For simplicity, we assume if a file with the same name exists, it's the same.
                        # For more robustness, you could compare file sizes or checksums.
                        logger.info(f"File '{filename}' already exists in Google Drive. Skipping.")
                        skipped_count += 1
                        continue # Skip to next file

                    # Create a PyDrive2 File object
                    gfile = drive_service.CreateFile({'title': filename, 'parents': [{'id': target_folder_id}]})
                    gfile.SetContentFile(file_path)
                    gfile.Upload()
                    uploaded_count += 1
                    logger.info(f"Successfully uploaded '{filename}' to Google Drive.")
                except Exception as e:
                    logger.error(f"Error uploading '{filename}': {e}", exc_info=True)
                    error_count += 1
            else:
                logger.debug(f"Skipping non-file entry: {filename}")

        logger.info(f"Log upload finished. Uploaded: {uploaded_count}, Skipped: {skipped_count}, Errors: {error_count}")

    # --- Main Execution ---
    if __name__ == '__main__':
        try:
            logger.info("Log Uploader script started.")
            # 1. Authenticate with Google Drive
            drive = authenticate_gdrive()
            logger.info("Successfully authenticated with Google Drive.")

            # 2. Upload logs
            upload_logs(drive, ROBOT_LOG_DIR, TARGET_FOLDER_ID)
            logger.info("Log Uploader script finished successfully.")
        except Exception as e:
            logger.critical(f"Log Uploader script failed critically: {e}", exc_info=True)
            sys.exit(1) # Exit with error code

    ```

3.  **IMPORTANT: Replace `YOUR_GOOGLE_DRIVE_FOLDER_ID`:**
    *   Open the `scripts/log_uploader.py` file.
    *   Find the line `TARGET_FOLDER_ID = 'YOUR_GOOGLE_DRIVE_FOLDER_ID'`
    *   Replace `'YOUR_GOOGLE_DRIVE_FOLDER_ID'` with the actual Folder ID you obtained in Phase 1, Step 6.
    *   Save the file.

---

## Phase 4: `systemd` Service Configuration

This phase sets up a `systemd` service to run your `log_uploader.py` script automatically on reboot.

1.  **Create the `systemd` Service File:**
    *   On your robot, create a new `systemd` service file:
        ```bash
        sudo nano /etc/systemd/system/robot-log-uploader.service
        ```

2.  **Paste the Service Configuration:**
    *   Paste the following content into the `nano` editor.

    ```
    [Unit]
    Description=Robot Log Uploader to Google Drive
    Requires=network-online.target
    After=network-online.target
    # This ensures the robot's main logging (robot_run.log) has a chance to finish writing initial logs
    After=hospital-robot.service 

    [Service]
    Type=oneshot
    User=root
    Group=root
    # Set the working directory to your robot's main code directory
    WorkingDirectory=/home/pi/Downloads/Robot_New_Repository_Update_knowledge_base-5

    # Path to the Python virtual environment and your upload script
    ExecStart=/home/pi/Downloads/Robot_New_Repository_Update_knowledge_base-5/.venv/bin/python 
              /home/pi/Downloads/Robot_New_Repository_Update_knowledge_base-5/scripts/log_uploader.py

    # Environment variables if needed, e.g., for log directory if not hardcoded in script
    # Environment=ROBOT_LOG_DIR=/var/log/robot

    StandardOutput=journal
    StandardError=journal
    TimeoutStartSec=300 # Give it plenty of time for network to be truly up and for uploads

    # Security hardening (optional but recommended)
    NoNewPrivileges=true
    ProtectSystem=full
    ProtectHome=true

    [Install]
    WantedBy=multi-user.target
    ```

3.  **Adjust Paths (if necessary):**
    *   In the `WorkingDirectory` and `ExecStart` lines above, make sure the paths match the actual location of your robot's project directory and virtual environment if they are different from `/home/pi/Downloads/Robot_New_Repository_Update_knowledge_base-5`.
    *   Save and exit `nano` (Ctrl+X, Y, Enter).

4.  **Reload `systemd` and Enable the Service:**
    *   Tell `systemd` about your new service:
        ```bash
        sudo systemctl daemon-reload
        ```
    *   Enable the service so it starts automatically on boot:
        ```bash
        sudo systemctl enable robot-log-uploader.service
        ```

5.  **Test the Service (without rebooting):**
    *   You can manually run the service to test it:
        ```bash
        sudo systemctl start robot-log-uploader.service
        ```
    *   Check its status and logs to see if it ran successfully:
        ```bash
        systemctl status robot-log-uploader.service
        journalctl -u robot-log-uploader.service -f
        ```
        *(Look for messages like "Log Uploader script started." and "Log upload finished.")*

6.  **Reboot and Verify:**
    *   Once you're confident it's working, reboot your robot:
        ```bash
        sudo reboot
        ```
    *   After the robot comes back online, check your Google Drive folder to see if the logs have been uploaded. Also, check the `systemctl status` and `journalctl` logs for the uploader service again to confirm it ran on boot.

You have now set up your robot to automatically upload its logs to Google Drive upon every reboot!