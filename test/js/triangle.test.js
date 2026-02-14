const axios = require("axios");

const BASE_URL = "http://127.0.0.1:5000/api/triangle";

describe("Triangle API Tests", () => {

  test("CCC valid triangle", async () => {
    const response = await axios.post(`${BASE_URL}/ccc`, {
      a: 3,
      b: 4,
      c: 5
    });

    expect(response.status).toBe(200);
    expect(response.data.valid).toBe(true);
    expect(response.data.area).toBeDefined();
  });

  test("CCC invalid triangle", async () => {
    try {
      await axios.post(`${BASE_URL}/ccc`, {
        a: 1,
        b: 2,
        c: 10
      });
    } catch (error) {
      expect(error.response.status).toBe(400);
    }
  });

  test("CGC valid", async () => {
    const response = await axios.post(`${BASE_URL}/cgc`, {
      a: 5,
      b: 7,
      angle_c: 60
    });

    expect(response.status).toBe(200);
    expect(response.data.valid).toBe(true);
  });

  test("Coordinates valid", async () => {
    const response = await axios.post(`${BASE_URL}/coords`, {
      x1: 0,
      y1: 0,
      x2: 4,
      y2: 0,
      x3: 1,
      y3: 3
    });

    expect(response.status).toBe(200);
    expect(response.data.valid).toBe(true);
  });

});
