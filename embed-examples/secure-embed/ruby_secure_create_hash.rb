require 'openssl'
require 'base64'
require 'json'
require 'uri'

def knowi_secure_hash(sso_key, plaintext)
  raise ArgumentError, 'SSO key must not be blank' if sso_key.nil? || sso_key.strip.empty?
  raise ArgumentError, 'Input text must not be blank' if plaintext.nil? || plaintext.strip.empty?

  # These bytes must match Knowi's Java helper.
  salt = [
    107, -50, -85, 33, -33, -115, -116, 37, 39, 33,
    33, -74, 117, -115, 20, -35, 74, -96, -4, -121
  ].pack('c*')
  iv = [
    -75, 16, 92, 14, 117, 74, -96, -4,
    -121, 38, 105, -65, 55, 24, 118, -45
  ].pack('c*')

  key = OpenSSL::PKCS5.pbkdf2_hmac_sha1(
    sso_key.encode('UTF-8'), salt, 1024, 16
  )

  cipher = OpenSSL::Cipher.new('AES-128-CBC')
  cipher.encrypt
  cipher.key = key
  cipher.iv = iv

  # OpenSSL applies PKCS#7 padding automatically (Java's PKCS5Padding for AES).
  encrypted = cipher.update(plaintext.encode('UTF-8')) + cipher.final
  Base64.strict_encode64(encrypted).gsub('/', '___')
end

if $PROGRAM_NAME == __FILE__
  # Choose filters on the server from the signed-in user's permitted data.
  content_filters = [
    { fieldName: 'Customer', values: ['Target'], operator: '=' }
  ]
  # Encode the value before encrypting, including any &, + or % characters.
  payload = URI.encode_www_form('contentFilters' => JSON.generate(content_filters))

  # Optional expiry: _t is epoch milliseconds; _ttl is seconds.
  # payload += "&_t=#{(Time.now.to_f * 1000).to_i}&_ttl=60"

  puts knowi_secure_hash(ENV.fetch('KNOWI_SSO_KEY'), payload)
end
