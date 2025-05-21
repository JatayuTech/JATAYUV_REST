document.addEventListener('DOMContentLoaded', function () {
    // Handle food suggestion toggle
    document.getElementById('foodSuggestion').addEventListener('change', function () {
        document.getElementById('foodDetails').style.display = this.value === 'Yes' ? 'block' : 'none';
    });

    // Show travel options dynamically
    window.showOptions = function (direction) {
        const pref = document.getElementById(`travelPreference${direction}`).value;
        document.getElementById(`busOptions${direction}`).style.display = pref === 'Bus' ? 'block' : 'none';
        document.getElementById(`trainOptions${direction}`).style.display = pref === 'Train' ? 'block' : 'none';
    };

    // Show accommodation sub-options
    document.getElementById('accommodationPreference').addEventListener('change', function () {
        document.getElementById('lowOptions').style.display = this.value === 'Low' ? 'block' : 'none';
    });

    // Form submission
    document.getElementById('travelForm').addEventListener('submit', async function (event) {
        event.preventDefault();

        const loadingOverlay = document.getElementById('loadingOverlay');
        const loading = document.getElementById('loading');
        loadingOverlay.style.display = 'flex';
        loading.style.display = 'block';

        try {
            const formData = {
                cId: Date.now(),
                cName: "Sample User",
                cSrc: document.getElementById('source').value,
                cDes: document.getElementById('destination').value,
                cTotalDays: parseInt(document.getElementById('days').value),
                cBudget: parseInt(document.getElementById('budget').value),
                cNsightseeing: parseInt(document.getElementById('sightseeing').value),
                cTravelPrf: document.getElementById('travelPreferenceOnward').value,
                cBusType: document.getElementById('busTypeOnward')?.value || null,
                cTrainCoach: document.getElementById('trainCoachOnward')?.value || null,
                cTravelStartTime: new Date().toISOString(),
                cTravelEndTime: new Date().toISOString(),
                cReturnTravelPrf: document.getElementById('travelPreferenceReturn').value,
                cReturnBusType: document.getElementById('busTypeReturn')?.value || null,
                cReturnTrainCoach: document.getElementById('trainCoachReturn')?.value || null,
                cReturnTravelStartTime: new Date().toISOString(),
                cReturnTravelEndTime: new Date().toISOString(),
                cAccomodationPrf: document.getElementById('accommodationPreference').value,
                cLowType: document.getElementById('lowType')?.value || null,
                cFoodSug: document.getElementById('foodSuggestion').value === 'Yes',
                cFoodChoice: document.getElementById('foodChoice')?.value || null
            };

            const response = await fetch("http://127.0.0.1:8000/saveClient", {
                method: "POST",
                headers: {
                    "Content-Type": "application/json"
                },
                body: JSON.stringify(formData)
            });

            const result = await response.json();

            // Prepare sightseeing output
            let sightseeingDetails = "<strong>Sightseeing Suggestions:</strong><br>";
            if (result[0]?.sightseeing_data?.length > 0) {
                result[0].sightseeing_data.forEach(item => {
                    sightseeingDetails += `• ${item.sPlace}, Entry Fee: ${item.sEnfee}, Distance: ${item.sDis}<br>`;
                });
            } else {
                sightseeingDetails += result[0]?.message || "No suggestions available.<br>";
            }

            // Prepare food output
            let foodDetails = "<strong>Food Suggestions:</strong><br>";
            if (result[1]?.filtered_food?.length > 0) {
                result[1].filtered_food.forEach(item => {
                    foodDetails += `• ${item.fItem} (${item.fResname})<br>`;
                });
            } else {
                foodDetails += result[1]?.message || "No food suggestions available.<br>";
            }

            // Show result on screen
            document.getElementById('resultText').innerHTML = `
                <h2>Your Trip Plan</h2>
                ${sightseeingDetails}<br>${foodDetails}
            `;
            document.getElementById('result').style.display = 'block';
            document.getElementById('resultOverlay').style.display = 'flex';
        } catch (error) {
            console.error("Error submitting form:", error);
            alert("An error occurred while sending the data.");
        } finally {
            loadingOverlay.style.display = 'none';
            loading.style.display = 'none';
        }
    });
});
