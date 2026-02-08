async function test() {
    try {
        const res = await fetch("http://127.0.0.1:8050/api/calculate", {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify({
                x1: 0,
                y1: 0,
                x2: 3,
                y2: 0,
                x3: 0,
                y3: 4
            })
        });

        const text = await res.text();
        console.log("Raw response:", text);

        const data = JSON.parse(text);
        console.log("JSON parsed:", data);

    } catch (err) {
        console.error("Error:", err);
    }
}

test();
