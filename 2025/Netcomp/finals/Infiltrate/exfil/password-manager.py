import os                                                                                                                                                                                                          
from cryptography.fernet import Fernet                                                                                                                                                                             
import json                                                                                                                                                                                                        
                                                                                                                                                                                                                   
# Fungsi untuk membuat key enkripsi baru                                                                                                                                                                           
def generate_key():                                                                                                                                                                                                
    return Fernet.generate_key()                                                                                                                                                                                   
                                                                                                                                                                                                                   
# Fungsi untuk menyimpan key enkripsi                                                                                                                                                                              
def save_key(key, filename="secret.key"):                                                                                                                                                                          
    with open(filename, "wb") as key_file:                                                                                                                                                                         
        key_file.write(key)                                                                                                                                                                                        
                                                                                                                                                                                                                   
# Fungsi untuk memuat key enkripsi yang sudah ada                                                                                                                                                                  
def load_key(filename="secret.key"):                                                                                                                                                                               
    if os.path.exists(filename):                                                                                                                                                                                   
        return open(filename, "rb").read()                                                                                                                                                                         
    else:                                                                                                                                                                                                          
        return None                                                                                                                                                                                                
                                                                                                                                                                                                                   
# Fungsi untuk mengenkripsi password                                                                                                                                                                               
def encrypt_password(password, key):                                                                                                                                                                               
    f = Fernet(key)                                                                                                                                                                                                
    encrypted_password = f.encrypt(password.encode())                                                                                                                                                              
    return encrypted_password                                                                                                                                                                                      
                                                                                                                                                                                                                   
# Fungsi untuk mendekripsi password                                                                                                                                                                                
def decrypt_password(encrypted_password, key):                                                                                                                                                                     
    f = Fernet(key)                                                                                                                                                                                                
    decrypted_password = f.decrypt(encrypted_password).decode()                                                                                                                                                    
    return decrypted_password                                                                                                                                                                                      
                                                                                                                                                                                                                   
# Fungsi untuk menyimpan password dalam file JSON                                                                                                                            
def save_password(service, username, encrypted_password, filename="passwords.json"):                                                                                         
    if os.path.exists(filename):                                                                                                                                             
        with open(filename, "r") as file:                                                                                                                                    
            data = json.load(file)                                                                                                                                           
    else:                                                                                                                                                                    
        data = {}                                                                                                                                                            
                                                                                                                                                                             
    data[service] = {"username": username, "password": encrypted_password.decode()}

    with open(filename, "w") as file:
        json.dump(data, file, indent=4)                                                                                                                                                                            

# Fungsi untuk mengambil password dari file JSON (case-insensitive)                                      
def get_password(service, key, filename="passwords.json"):                                               
    if os.path.exists(filename):                    
        with open(filename, "r") as file:           
            data = json.load(file)                  
                                                    
        # Konversi nama service menjadi lowercase                                                        
        service = service.lower()                   

        # Cari service yang sesuai (case-insensitive)                                                    
        for stored_service in data:                 
            if stored_service.lower() == service:                                                        
                encrypted_password = data[stored_service]["password"].encode()                           
                username = data[stored_service]["username"]                                              
                decrypted_password = decrypt_password(encrypted_password, key)                           
                return username, decrypted_password                                                      
                                                    
        return None, None                           
    else:                                           
        return None, None                           

# Program utama                                     
def main():                                         
    key = load_key()  # Muat kunci jika ada                                                              
    if not key:  # Jika kunci belum ada, buat kunci baru dan simpan                                      
        key = generate_key()                        
        save_key(key)                               

    while True:                                     
        print("\nPassword Manager")                 
        print("1. Add Password")                    
        print("2. Get Password")                    
        print("3. Exit")                            

        choice = input("Select an option: ")                                                             

        if choice == "1":                           
            service = input("Enter service name (e.g., Gmail): ")                                        
            username = input("Enter username: ")                                                         
            password = input("Enter password: ")                                                         
            encrypted_password = encrypt_password(password, key)                                         
            save_password(service, username, encrypted_password)                                         
            print(f"Password for {service} saved successfully.")
        elif choice == "2":                         
            service = input("Enter service name to retrieve password: ")                                 
            username, decrypted_password = get_password(service, key)                                    
            if username:                            
                print(f"Username: {username}")                                                           
                print(f"Password: {decrypted_password}")                                                 
            else:                                   
                print("No password found for this service.")                                             

        elif choice == "3":                         
            break                                   
        else:                                       
            print("Invalid option, please try again.")                                                   

if __name__ == "__main__":                          
    main()           