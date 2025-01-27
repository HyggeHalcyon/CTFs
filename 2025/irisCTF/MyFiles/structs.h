struct user {
    char *username;
    char *password;
    int is_admin;
    int num_of_files;
};

struct zip_header {
    int sig;
    short ver;
    short flags;
    short compression;
    short mod_time;
    short mod_date;
    int crc_32;
    int compressed_size;
    int uncompressed_size;
    short filename_len; // or long (?)
};

struct zipfile {
    unsigned int zip_size;
    struct zip_header header;
    char content[0x200-sizeof(struct zip_header)]; 
};

struct file_user {
    struct user user;
    struct zipfile files[0x100];
};

struct file_info {
    char *filename;
    unsigned long file_size;
    long hash;
};