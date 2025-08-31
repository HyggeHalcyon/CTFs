#include <stdint.h>
#include <string.h>


static const char alpha_map[] = "ZYXWVUTSRQPONMLKJIHGFEDCBAabcdefghijklmnopqrstuvwxyz";
static const char num_map[] = "9876543210";

static const uint32_t MAGIC_PRIME = 0x1F2F3F4F;
static const uint32_t VALIDATION_KEY = 0x41424344;
static const uint32_t TIME_SEED = 1640995200; 

uint32_t djb2_hash(const char* str, int len) {
    uint32_t hash = 5381;
    for (int i = 0; i < len; i++) {
        hash = ((hash << 5) + hash) + str[i];
    }
    return hash;
}

uint32_t fnv1a_hash(const char* str, int len) {
    uint32_t hash = 2166136261u;
    for (int i = 0; i < len; i++) {
        hash ^= str[i];
        hash *= 16777619;
    }
    return hash;
}

uint32_t combined_hash(const char* str, int len) {
    uint32_t djb2 = djb2_hash(str, len);
    uint32_t fnv1a = fnv1a_hash(str, len);
    uint32_t combined = djb2 ^ fnv1a;
    combined = (combined << 13) | (combined >> 19);
    
    return combined ^ MAGIC_PRIME;
}

int uint_to_string(uint32_t num, char* str) {
    if (num == 0) {
        str[0] = '0';
        str[1] = '\0';
        return 1;
    }
    
    char temp[16];
    int i = 0;
    while (num > 0) {
        temp[i++] = '0' + (num % 10);
        num /= 10;
    }
    
    for (int j = 0; j < i; j++) {
        str[j] = temp[i - 1 - j];
    }
    str[i] = '\0';
    
    return i;
}

uint8_t calculate_checksum(const char* data, int len) {
    uint32_t checksum = 0;
    for (int i = 0; i < len; i++) {
        checksum += data[i] * (i + 1) * 17;
    }
    return (checksum ^ (checksum >> 8) ^ (checksum >> 16)) & 0xFF;
}

char transform_char(char c, int position) {
    if (c >= 'A' && c <= 'Z') {
        int idx = c - 'A';
        return alpha_map[idx] ^ (position & 0x1F);
    } else if (c >= 'a' && c <= 'z') {
        int idx = 26 + (c - 'a');
        return alpha_map[idx] ^ (position & 0x1F);
    } else if (c >= '0' && c <= '9') {
        return num_map[c - '0'] ^ (position & 0x0F);
    }
    return c ^ (position & 0x07);
}

int validate_username_format(const char* username, int len) {
    if (len < 6 || len > 10) return 0;
    
    int letter_count = 0, digit_count = 0;
    for (int i = 0; i < len; i++) {
        if ((username[i] >= 'A' && username[i] <= 'Z') || 
            (username[i] >= 'a' && username[i] <= 'z')) {
            letter_count++;
        } else if (username[i] >= '0' && username[i] <= '9') {
            digit_count++;
        }
    }
    if (letter_count < 2 || digit_count < 1) return 0;
    
    uint32_t ascii_sum = 0;
    for (int i = 0; i < len; i++) {
        ascii_sum += username[i];
    }
    if (ascii_sum < 400 || ascii_sum > 800) return 0;
    uint32_t hash = combined_hash(username, len);
    if (hash % 42 != 0) return 0;
    if ((hash & 0xFF) != 0x7E) return 0;
    
    return 1;
}

uint32_t generate_expected_password(const char* username, int len) {
    uint32_t base_hash = combined_hash(username, len);
    uint8_t checksum = calculate_checksum(username, len);
    uint32_t transformed = base_hash ^ (checksum * 0x01010101);
    transformed ^= TIME_SEED;
    transformed = (transformed * 0x41C64E6D) + 0x3039;
    transformed ^= VALIDATION_KEY;
    return (transformed % 999999) + 100000;
}

int verify_credentials(const char* username, int username_len, uint32_t password) {
    if (!validate_username_format(username, username_len)) {
        return 0;
    }
    uint32_t expected = generate_expected_password(username, username_len);
    if (password != expected) {
        return 0;
    }
    uint32_t digit_sum = 0;
    uint32_t temp = password;
    while (temp > 0) {
        digit_sum += temp % 10;
        temp /= 10;
    }
    if (digit_sum % 7 != 0) return 0;
    char pwd_str[8];
    uint_to_string(password, pwd_str);
    int pwd_len = strlen(pwd_str);
    int is_palindrome = 1;
    for (int i = 0; i < pwd_len / 2; i++) {
        if (pwd_str[i] != pwd_str[pwd_len - 1 - i]) {
            is_palindrome = 0;
            break;
        }
    }
    if (is_palindrome) return 0;
    
    return 1;
}
__attribute__((export_name("authenticate")))
int authenticate(uint32_t username_ptr, uint32_t username_len, uint32_t password) {
    char* username = (char*)username_ptr;
    if (username_len > 50 || username_len < 1) {
        return 0;
    }
    return verify_credentials(username, username_len, password);
}
__attribute__((export_name("get_expected_password")))
uint32_t get_expected_password(uint32_t username_ptr, uint32_t username_len) {
    char* username = (char*)username_ptr;
    if (username_len > 50 || username_len < 1) {
        return 0;
    }
    if (!validate_username_format(username, username_len)) {
        return 0;
    }
    
    return generate_expected_password(username, username_len);
}
__attribute__((export_name("get_username_hash")))
uint32_t get_username_hash(uint32_t username_ptr, uint32_t username_len) {
    char* username = (char*)username_ptr;
    
    if (username_len > 50 || username_len < 1) {
        return 0;
    }
    
    return combined_hash(username, username_len);
}