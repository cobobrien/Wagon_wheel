
function cart(item){
    var item_id = item.getAttribute('data-id');
    var item_size = item.getAttribute('data-size');

    const request = new XMLHttpRequest();

    request.open('POST', '/cart');
    // Callback function for when request completes
    request.onload = () => {
      // Extract JSON data from request
      const data = JSON.parse(request.responseText);
      // Update the result div
      if (data.success) {
         var hasChild = document.getElementById("cart_items_list").querySelector("#empty_cart");
         if(hasChild)
            hasChild.remove();
         var hasTotal = document.getElementById("order_total");
         if(hasTotal)
            hasTotal.remove();
         const p_name = document.createElement('li');
         p_name.innerHTML = data.cart_item + ": $" + data.price;
         p_name.className = "border border-light rounded";
         const order_total = document.createElement('p');
         order_total.id = "order_total";
         order_total.innerHTML =  "<b>Total: " + data.order_total + "</b>";
         order_total.className = "ml-1 mt-auto";
         document.querySelector("#cart_items_list").append(p_name);
         document.querySelector("#cart_items_list").append(order_total);
         var order_items = document.querySelector("#cart");
         order_items.innerHTML = "Cart(" + data.order_items + ")";
      }
      else {
         alert("unsuccessful");
      }
    }
    // Add data to send with request
    var csrftoken = Cookies.get('csrftoken');
    request.setRequestHeader("X-CSRFToken", csrftoken);
    const data = new FormData();
    data.append('item_id', item_id);
    data.append('item_size', item_size);
    // Send request
    request.send(data);
}

function addTopping(topping){
    return;
}

document.addEventListener('DOMContentLoaded', function() {
    cart_container = document.getElementById("cart_container");
    cart_container.style.visibility='hidden';
    document.querySelector('#cart').onclick = () => {
       cart_container = document.getElementById("cart_container");
       if (cart_container.style.visibility=='hidden')
           cart_container.style.visibility='visible';
       else
           cart_container.style.visibility='hidden';
    }
    cart_items_list = document.getElementById("cart_items_list");
    if (!cart_items_list.hasChildNodes()){
        const p_empty = document.createElement('p');
        p_empty.innerHTML = "There are no items in your cart";
        p_empty.style = "text-align: center; margin: auto; padding: 1rem";
        p_empty.id = "empty_cart"
        document.querySelector("#cart_items_list").append(p_empty);
    }
})