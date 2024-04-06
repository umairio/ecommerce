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
