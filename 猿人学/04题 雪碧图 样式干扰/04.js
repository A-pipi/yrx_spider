const crypto = require("crypto");


md5 = function(str) {
    let s = crypto.createHash("md5").update(str).digest("hex");
    return s;
}

function encrypt(key, value) {
    let j_key = '.' + md5(btoa(key + value).replace(/=/g, ''));
    return j_key.split(".")[1];
}

mi = encrypt("Ip8Iki3grF", "b12hgw8ztI");
console.log(mi)
// af96306605bbc0867c6b5687f73d9730
