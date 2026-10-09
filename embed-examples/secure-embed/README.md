# Secure embedding samples

These examples generate the encrypted hash used by Knowi secure dashboard and widget embeds.

## Ruby

[ruby_secure_create_hash.rb](ruby_secure_create_hash.rb) generates the hash on your application server without a Management API call. It requires Ruby with OpenSSL support.

1. Enable **Secure Shareable URL** in the dashboard's Sharing Options and save.
2. Set `KNOWI_SSO_KEY` in your server's environment to the customer SSO key from **User Management > Customer settings**. Keep this key out of browser code and source control.
3. Replace the sample `content_filters` with filters derived from the signed-in user's permitted data. Authorize these values on your backend before generating a hash.
4. From the repository root, run:

   ```sh
   ruby embed-examples/secure-embed/ruby_secure_create_hash.rb
   ```

The script prints the hash. The `knowi_secure_hash(sso_key, plaintext)` function can also be loaded with `require_relative` without running the example.

The payload is a form-encoded query string. Encode each parameter value before encryption so characters such as `&`, `+`, `%`, and Unicode survive parsing. The script includes an optional expiry: `_t` is the issue time in epoch milliseconds and `_ttl` is the lifetime in seconds.

### Use the hash

In the secure URL `/share/secure/<dashboard-token>/<secure-hash>`, use the dashboard token from Sharing Options and replace the hash with the Ruby-generated value.

For JavaScript embedding, load the Knowi JavaScript library and provide a container:

```html
<script src="https://knowi.com/minify/knowi-api.min.js"></script>
<div id="knowi-div"></div>
<script>
  Knowi.render('#knowi-div', {
    type: 'secure',
    dashboard: '<dashboard-token>',
    hash: '<hash-generated-by-ruby>'
  });
</script>
```

Return the generated hash to your frontend; keep the SSO key on your server. For a secure widget, use `type: 'shareWidgetSecure'` with the widget's share token in `dashboard`.

### Java compatibility

The Ruby helper matches [java_SecureEmbedHashEncryption.java](java_SecureEmbedHashEncryption.java): PBKDF2-HMAC-SHA1 with 1,024 iterations and a 16-byte key, AES-128-CBC with the same salt and IV, and standard Base64 with `/` replaced by `___`. Preserve these settings for compatibility with Knowi's secure URL format. OpenSSL supplies the padding automatically; do not add manual padding.
