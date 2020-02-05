// Knowi helper class to generate an encryption key for use 
// with secure dashboard/widget embedding


package com.knowi;

import javax.crypto.Cipher;
import javax.crypto.SecretKey;
import javax.crypto.SecretKeyFactory;
import javax.crypto.spec.IvParameterSpec;
import javax.crypto.spec.PBEKeySpec;
import javax.crypto.spec.SecretKeySpec;
import java.security.Key;
import java.util.Base64;


public class EncryptUtil {

    private static final byte[] SALT =
            new byte[]{107, -50, -85, 33, -33, -115, -116, 37, 39, 33, 33, -74, 117, -115, 20, -35, 74, -96, -4, -121};
    private static final int KEY_ITERATION_COUNT = 1024;
    private static final int KEY_SIZE = 128;
    private static final String KEY_ALGORITHM = "PBKDF2WithHmacSHA1";
    private static final String KEY_TRANSFORMATION = "AES/CBC/PKCS5Padding";
    private static final String KEY_PROTOCOL = "AES";
    private static final byte[] CIPHER_IVY =
            new byte[]{-75, 16, 92, 14, 117, 74, -96, -4, -121, 38, 105, -65, 55, 24, 118, -45};

    public static String encrypt(Key key, String plainText) {
        if (plainText == null || plainText.trim().isEmpty()) {
            throw new IllegalArgumentException("Input text can't be empty");
        }
        try {
            Cipher cipher = Cipher.getInstance(KEY_TRANSFORMATION);
            cipher.init(Cipher.ENCRYPT_MODE, key, new IvParameterSpec(CIPHER_IVY));

            byte[] encryptedTextBytes = cipher.doFinal(plainText.getBytes("UTF-8"));
            return Base64.getEncoder().encodeToString(encryptedTextBytes);
        } catch (Exception e) {
            System.err.println("Error while encrypting message: " + plainText);
            e.printStackTrace();
            throw new RuntimeException("Error while encrypting message: " + plainText, e);
        }
    }


    public static Key generateKey(String connectorId) {
        return generateKey(connectorId, null);
    }

    private static Key generateKey(String password, byte[] salt) {
        try {
            if (salt == null) {
                salt = SALT;
            }
            PBEKeySpec spec = new PBEKeySpec(password.toCharArray(), salt, KEY_ITERATION_COUNT, KEY_SIZE);

            SecretKeyFactory factory = SecretKeyFactory.getInstance(KEY_ALGORITHM);
            SecretKey secretKey = factory.generateSecret(spec);
            return new SecretKeySpec(secretKey.getEncoded(), KEY_PROTOCOL);
        } catch (Exception e) {
            System.err.println("Failed to create encryption key");
            e.printStackTrace();
            throw new RuntimeException("Failed to create encryption key", e);
        }
    }

    public static void main(String[] args) throws Exception {
        String a = "contentFilters=[{\"fieldName\": \"Customer\", \"values\": [\"Target\"], \"operator\":\"=\"}]"; // replace with content filters

        String secureHash = EncryptUtil.encrypt(EncryptUtil.generateKey("CUSTOMER_TOKEN_HERE"), a); // update with Knowi Customer Token
        System.err.println(secureHash.replaceAll("/", "___"));
    }
}

