typedef struct {
    long balance;
    long id;
    char name[16];
    void* func;
} person;

typedef struct {
    char tag[32];
    long total;
} order;

typedef struct {
    char state[16];
    long length;
    long number;
    long zip;
    char city[16];
    char full_address[];
} address;