from datetime import datetime
import configs
import logging
import paramiko
import os


def sftp_transfer():
    privateKeyFilePath_internet = 'XXXX'
    privateKeyFilePath_intranet = 'XXXX'
    print 'Inside Function'
    logging.basicConfig(filename='Client.log',level=logging.INFO, format='%(asctime)s %(message)s', datefmt='%m/%d/%Y %I:%M:%S %p :')
    print 'After Log Config' 
    try:
	  print 'Inside Try'
	  logging.info('Going to Source Host')
    source_host = configs.source_sftp_hostname 
    source_port = 8022
    source_username = configs.source_username

    dest_host = configs.dest_sftp_hostname 
            
    dest_port = 8022
    dest_username = configs.dest_username 
    # Create SSH clients for both source and destination accounts
    source_client = paramiko.SSHClient()
    source_client.set_missing_host_key_policy(paramiko.AutoAddPolicy())

    dest_client = paramiko.SSHClient()
    dest_client.set_missing_host_key_policy(paramiko.AutoAddPolicy())

    # Load private keys for both source and destination accounts
    source_key = paramiko.RSAKey.from_private_key_file(privateKeyFilePath_internet)
    dest_key = paramiko.RSAKey.from_private_key_file(privateKeyFilePath_intranet)
	  print 'Before Source Client'
    # Connect to source account
    source_client.connect(source_host, port=source_port, username=source_username, pkey=source_key)
    # Connect to destination account
    dest_client.connect(dest_host, port=dest_port, username=dest_username, pkey=dest_key)
	  print 'Destination Client Connected'
    logging.info('Connection successfully established ... ')
    # Set up SFTP connections for both accounts
    source_sftp = source_client.open_sftp()
    dest_sftp = dest_client.open_sftp()
    # Define source and destination paths
    dest_file_path = configs.outgoing_file_path
    incom_file_path = configs.incoming_file_path
	  print 'Incoming File Path ' + ignite_incom_file_path
    remoteArchiveFilePath = configs.archive_file_path
    today = datetime.now()
    backup_folder = remoteArchiveFilePath+ '/' + today.strftime('%d-%m-%Y')
	  print 'Backup Folder '+backup_folder
    if today.strftime('%d-%m-%Y') not in source_sftp.listdir(remoteArchiveFilePath):
        source_sftp.mkdir(backup_folder) 
    value =[]        
    for file in source_sftp.listdir_attr(incom_file_path): 
        value.append(file.filename)
        logging.info('Transferring file name ' + file.filename)
  	    print 'Transferring file name ' + file.filename
  	    dest_file_path = str(dest_file_path + '/'+ file.filename)
  	    print 'Dest' + dest_file_path
  	    source_file_path = str(incom_file_path +'/'+ file.filename)
  	    logging.info('Source file path ' + source_file_path)
  	    print 'Filename'+file.filename
  	    local_path = 'Download' + '/'+ file.filename
  	    print 'LocalPath' +local_path
  	    source_sftp.get(source_file_path, local_path)
  	    print 'Download Done'
  	    source_sftp.rename(source_file_path,backup_folder +'/'+ file.filename)
  	    print 'Rename Done'
  	    dest_sftp.put(local_path, dest_file_path)
  	    print 'Upload Done'
  	    os.remove(local_path)
  	    source_sftp.close()
        dest_sftp.close()

        # Close SSH connections
        source_client.close()
        dest_client.close()     
    except Exception as ex:
        logging.error(ex)
	print ex

if __name__ == '__main__':   
    sftp_transfer()
    




                 


