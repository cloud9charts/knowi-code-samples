const request = require('request');
const HOST = "https://knowi.com/api/1.0";

// update the following with actual values for client id/secret, dashboard id, content filter
const clientID = "<knowi_client_id>";
const clientSecret = "<knowi_client_secret>";
const dashboardId = "<knowi_dashboard_id>";
const contentFilter = [
    {fieldName: "customer", values: ["EU Atlantic", "Knowi Airways"], operator: "="},
    {fieldName: "status", values: ["Rejected"], operator: "="}
];

function dashboardSecureHash() {
    request.post(HOST + '/login', {
            form: {"client_id": clientID, "client_secret": clientSecret}
        }
        , (err, res, body) => {
            if (res.statusCode === 200) {

                request.post({
                    url: HOST + `/dashboards/${dashboardId}/share/url/secure`,
                    headers: {"Authorization": `Bearer ${JSON.parse(body).access_token}`},
                    form: {"contentFilters": JSON.stringify(contentFilter)}
                }, (err, res, body) => {
                    console.log(body);
                    var hash = (JSON.parse(body));

                    console.log(`https://www.knowi.com/share/secure/${hash.secureShareUrl}`)
                });

            } else {
                console.log(res.statusCode, body);
            }

        }
    )
}

dashboardSecureHash();