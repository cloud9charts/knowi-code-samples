const crypto = require('crypto');

const SALT = Buffer.from([107, -50, -85, 33, -33, -115, -116, 37, 39, 33, 33, -74, 117, -115, 20, -35, 74, -96, -4, -121]);
const KEY_ITERATION_COUNT = 1024;
const KEY_SIZE = 16; // In Node.js, AES-128 requires a 16-byte key
const KEY_ALGORITHM = 'aes-128-cbc';
const CIPHER_IVY = Buffer.from([-75, 16, 92, 14, 117, 74, -96, -4, -121, 38, 105, -65, 55, 24, 118, -45]);

function encrypt(key, plainText) {
    if (!plainText || plainText.trim().length === 0) {
        throw new Error('Input text can\'t be empty');
    }

    try {
        const cipher = crypto.createCipheriv(KEY_ALGORITHM, key, CIPHER_IVY);
        let encryptedText = cipher.update(plainText, 'utf8', 'base64');
        encryptedText += cipher.final('base64');
        return encryptedText;
    } catch (error) {
        console.error('Error while encrypting message: ', plainText);
        console.error(error);
        throw new Error('Error while encrypting message: ' + plainText);
    }
}

function generateKey(password, salt) {
    try {
        if (!salt) {
            salt = SALT;
        }
        const derivedKey = crypto.pbkdf2Sync(password, salt, KEY_ITERATION_COUNT, KEY_SIZE, 'sha1');
        return derivedKey;
    } catch (error) {
        console.error('Failed to create encryption key');
        console.error(error);
        throw new Error('Failed to create encryption key');
    }
}

function main() {
    const a = 'contentFilters=[{"fieldName": "Customer", "values": ["Target"], "operator":"="}]'; // replace with content filters
    const key = generateKey('08b1721058b0490e8808b232ea4931d5');
    const secureHash = encrypt(key, a);
    console.log(secureHash.replace(/\//g, '___'));
}

main();

