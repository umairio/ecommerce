const get_product_info = async (productId) => {
  try {
    const res = await fetch(`http://127.0.0.1:8000/api/product/${productId}`, {
      method: "GET",
      headers: {
        Authorization: "Bearer " + localStorage.getItem("accessToken"),
        "Content-Type": "application/json",
      },
    });

    const data = res.json();
    return data;
  } catch (error) {
    console.log(error);
  }
};

const get_order_info = async (orderId) => {
  try {
    const res = await fetch(`http://127.0.0.1:8000/api/order/${orderId}`, {
      method: "GET",
      headers: {
        Authorization: "Bearer " + localStorage.getItem("accessToken"),
        "Content-Type": "application/json",
      },
    });

    const data = res.json();
    return data;
  } catch (error) {
    console.log(error);
  }
};

const get_review_info = async (reviewId) => {
  try {
    const res = await fetch(`http://127.0.0.1:8000/api/review/${reviewId}`, {
      method: "GET",
      headers: {
        Authorization: "Bearer " + localStorage.getItem("accessToken"),
        "Content-Type": "application/json",
      },
    });

    const data = res.json();
    return data;
  } catch (error) {
    console.log(error);
  }
};

const get_user_info = async (userId) => {
  try {
    const res = await fetch(`http://127.0.0.1:8000/api/user/${userId}`, {
      method: "GET",
      headers: {
        Authorization: "Bearer " + localStorage.getItem("accessToken"),
        "Content-Type": "application/json",
      },
    });
    const data = res.json();
    return data;
  } catch (error) {
    console.log(error);
  }
};

const get_shop_info = async (shopId) => {
  try {
    const res = await fetch(`http://127.0.0.1:8000/api/shop/${shopId}`, {
      method: "GET",
      headers: {
        Authorization: "Bearer " + localStorage.getItem("accessToken"),
        "Content-Type": "application/json",
      },
    });
    const data = res.json();
    return data;
  } catch (error) {
    console.log(error);
  }
};
const get_profile_by_user = async (userId) => {
  try {
    const res = await fetch(
      `http://127.0.0.1:8000/api/profile/?user=${userId}`,
      {
        method: "GET",
        headers: {
          Authorization: "Bearer " + localStorage.getItem("accessToken"),
          "Content-Type": "application/json",
        },
      }
    );
    const data = res.json();
    return data;
  } catch (error) {
    console.log(error);
  }
};

const request_user = async () => {
  try {
    const res = await fetch(`http://127.0.0.1:8000/api/authuser/`, {
      method: "GET",
      headers: {
        Authorization: "Bearer " + localStorage.getItem("accessToken"),
        "Content-Type": "application/json",
      },
    });
    const data = res.json();
    return data;
  } catch (error) {
    console.log(error);
  }
};
