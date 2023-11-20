const lang = window.navigator.language;
console.log(lang);
function apiAuth() {
    if (!window.h5sdk) {
        console.log('invalid h5sdk')
        alert('please open in lark')
        return
    }
    //console.log("here: apiAuth");

    // Use Route: get_appid on the server-side to get the app_id
    // For more information on Route: get_appid , see the get_appid() function of the server module server.py .
    // For security, do not disclose the app_id  and never write it in plaintext on the front-end. Therefore, this parameter is obtained from the server.
    fetch(`/auth/get_appid`).then(response1 => response1.json().then(res1 => {
        console.log("get appid succeed: ", res1.appid);
        // Use the error API to handle the callback after the failure of API authentication.
        window.h5sdk.error(err => {
            throw('h5sdk error:', JSON.stringify(err));
        });
        // Use the ready API to confirm that the environment is ready before calling the API.
        window.h5sdk.ready(() => {
            console.log("window.h5sdk.ready");
            console.log("url:", window.location.href);
            // Call JSAPI tt.requestAuthCode to get authorization code
            tt.requestAuthCode({
                appId: res1.appid,
                // Success callback
                success(res) {
                    console.log("getAuthCode succeed");
                    //authorization code is stored in res.code.
                    // Pass code to Route: callbackof Web App Server using fetch and obtain user_info.
                    // For more information on Route: callback , see the callback() function of server module server.py.
                    
                    fetch(`/auth/callback?code=${res.code}`).then(response2 => response2.json().then(res2 => {
                        console.log("getUserInfo succeed");
                        window.location.href = '/auth/';} // redirect to auth, should be already login and pass the auth
                        // In the Demo , showUser, a separately defined parameter, is used to display user information on front-end pages.
                        //showUser(res2);}
                        )
                    ).catch(function(e) {console.error(e)})
                },
                // Failure callback
                fail(err) {
                    console.log(`getAuthCode failed, err:`, JSON.stringify(err));
                }
            })
        }
        )
    })).catch(function (e) { // Handling of the failure to get the app_id from the server
        console.error(e)
        })
}
function showUser(res) {
    // Display user information
    $('#img_div').html(`<img src="${res.avatar_url}" width="100%" height=""100%/>`);
    $('#hello_text_name').text(lang === "zh_CN" || lang === "zh-CN" ? `${res.name}` : `${res.en_name}`);
    $('#hello_text_welcome').text(lang === "zh_CN" || lang === "zh-CN" ? "欢迎使用 Lark" : "welcome to Lark");
}