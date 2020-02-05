const request = require('request');
require('dotenv').config();
const HOST = "https://knowi.com";
const KNOWI_CUSTOMER_TOKEN = process.env.KNOWI_CUSTOMER_TOKEN; // # update with Knowi Customer Token
const EMAIL = 'email@commpany.com'; // # email of single sign on user to create


function createSsoUserAndSession(email) {
    request.post(HOST + '/sso/user/create', {
            form: {
                'user': email,
                'ssoCustomerToken': KNOWI_CUSTOMER_TOKEN,
            }
        }
        , (err, res, body) => {
            if (res.statusCode === 200) {
                console.log(`*** NEW SSO USER TOKEN CREATED: ${body} ***`);
                request.post(HOST + '/sso/session/create', {
                    form: {
                        'user': email,
                        'userToken': body
                    }
                }, (err, res, body) => {
                    console.log(`*** NEW SSO USER SESSION CREATED: ${body} ***`);
                    console.log(`login url: ${HOST}/sso/user/login?token=${body}`);
                });
            } else {
                console.log('Error occurred creating user', res.statusMessage);
            }
        }
    )
}

createSsoUserAndSession(EMAIL);