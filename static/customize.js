document.getElementById('customMilkshakeForm').addEventListener('submit', function(event) {
    event.preventDefault();
    const base = document.getElementById('base').value;
    const milk = document.getElementById('milk').value;
    const toppings = document.getElementById('toppings').value;
    const size = document.getElementById('size').value;
    const Customer_name = document.getElementById('name').value;

    alert(`Your milkshake: Base - ${base}, Milk - ${milk}, Toppings - ${toppings}, Size - ${size}, Name - ${Customer_name},`);
});