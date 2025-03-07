// Fetch fridge items and display them
async function fetchFridgeItems() {
    try {
        const response = await fetch('/get_fridge_items');
        if (!response.ok) {
            throw new Error('Network response was not ok');
        }
        const fridgeItems = await response.json();
        displayFridgeItems(fridgeItems);
    } catch (error) {
        console.error('Error fetching fridge items:', error);
    }
}

// Display fridge items
function displayFridgeItems(fridgeItems) {
    const fridgeDiv = document.getElementById('fridge-items');
    fridgeDiv.innerHTML = '<h2>Items in Your Fridge:</h2>';
    for (const [name, quantity] of Object.entries(fridgeItems)) {
        fridgeDiv.innerHTML += `<p>${name}: ${quantity}</p>`;
    }
}

// Get recipes based on user input
document.getElementById('get-recipes').addEventListener('click', async () => {
    const budget = document.getElementById('budget').value;

    // Fetch fridge items again to get the latest ingredients
    const response = await fetch('/get_fridge_items');
    const fridgeItems = await response.json();
    const ingredients = Object.keys(fridgeItems); // Get ingredient names

    const recipesResponse = await fetch('/get_recipes', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({ ingredients, budget }),
    });

    const recipesData = await recipesResponse.json();
    displayRecipes(recipesData);
});

// Display recipes
function displayRecipes(data) {
    const recipesDiv = document.getElementById('recipes');
    recipesDiv.innerHTML = ''; // Clear previous results

    if (data.error) {
        recipesDiv.innerHTML = `<p>Error: ${data.error}</p>`;
        return;
    }

    const recipes = data.recipes || [];
    recipes.forEach(recipe => {
        const recipeElement = document.createElement('div');
        recipeElement.innerHTML = `<h3>${recipe.title}</h3><p>${recipe.description}</p>`;
        recipesDiv.appendChild(recipeElement);
    });
}

// Call the function to fetch fridge items when the page loads
window.onload = fetchFridgeItems;