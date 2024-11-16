
window.onload = async function() {
    const response = await fetch('/get_flavors');
    const data = await response.json();
    const flavorList = document.getElementById('flavor-list');
    data.flavors.forEach(flavor => {
        const li = document.createElement('li');
        li.textContent = `${flavor[1]} (${flavor[2]}) - Available from: ${flavor[3]} to ${flavor[4]}`;
        flavorList.appendChild(li);
    });
    

    const ingredientResponse = await fetch('/get_ingredients');
    const ingredientData = await ingredientResponse.json();
    const ingredientList = document.getElementById('ingredient-list');
    ingredientData.ingredients.forEach(ingredient => {
        const li = document.createElement('li');
        li.textContent = `${ingredient[1]} - Quantity: ${ingredient[2]}`;
        ingredientList.appendChild(li);
    });
};

const ingredientForm = document.getElementById('ingredient-form');
if (ingredientForm) {
    ingredientForm.onsubmit = async function(event) {
        event.preventDefault();

        const name = document.getElementById('ingredient-name').value;
        const quantity = document.getElementById('ingredient-quantity').value;

        const response = await fetch('/add_ingredient', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ name: name, quantity: quantity })
        });

        if (response.ok) {
            alert("Ingredient added successfully!");
            window.location.reload();  
        } else {
            alert("Error adding ingredient.");
        }
    };
}


const suggestionForm = document.getElementById('suggestion-form');
if (suggestionForm) {
    suggestionForm.onsubmit = async function(event) {
        event.preventDefault();

        const suggestion = document.getElementById('suggestion').value;
        const allergies = document.getElementById('allergies').value;

        const response = await fetch('/add_suggestion', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ flavor_suggestion: suggestion, allergies: allergies })
        });

        if (response.ok) {
            alert("Your suggestion has been submitted!");
            suggestionForm.reset();
        } else {
            alert("Error submitting suggestion.");
        }
    };
}
