const safeExtract = (a, b, c) => {
    if (a === null || a === undefined) return null;
    
    let val = a; 
    if (b !== null && b !== undefined && c !== null && c !== undefined) {
        val += b * Math.sqrt(c);
    }
    return val;
};



const toRad = (deg) => (deg * Math.PI) / 180;



window.dash_clientside = window.dash_clientside || {};
window.dash_clientside.clientside = {
    // Viết thẳng các hàm vào đây luôn
    check_ccc: function(...vals) {
        const v1 = safeExtract(vals[0], vals[1], vals[2]);
        const v2 = safeExtract(vals[3], vals[4], vals[5]);
        const v3 = safeExtract(vals[6], vals[7], vals[8]);

        const isReady = (v1 !== null && v2 !== null && v3 !== null && v1 > 0 && v2 > 0 && v3 > 0);
        return [v1, v2, v3, !isReady];
    },

    check_cgc: function(...vals) {
        const v1 = safeExtract(vals[0], vals[1], vals[2]);
        const v2 = safeExtract(vals[3], vals[4], vals[5]);
        const angle = vals[6];

        const isValid = (
            v1 !== null && v1 > 0 &&
            v2 !== null && v2 > 0 &&
            angle !== null && angle > 0 && angle < 180
        );
        return [v1, v2, !isValid];
    },

    check_gcg: function(...vals) {
        const valC = safeExtract(vals[0], vals[1], vals[2]);
        const g1 = vals[3];
        const g2 = vals[4];

        const isValid = (
            valC !== null && valC > 0 &&
            g1 !== null && g1 > 0 &&
            g2 !== null && g2 > 0 &&
            (g1 + g2) < 180
        );
        return [valC, !isValid];
    }
};