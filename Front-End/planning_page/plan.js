// plan.js
document.addEventListener('DOMContentLoaded', function () {
    const API_BASE_URL = "http://127.0.0.1:8002";

    flatpickr(".time-picker", {
        enableTime: true,
        noCalendar: true,
        dateFormat: "H:i",
        time_24hr: true,
        allowInput: true
    });

    // Global state variables
    let structuredPlans = [];
    let numberOfPlans = 0;
    let userSelectedTotalDays = 0;

    let tripSource = "";
    let tripDestination = "";

    let allSightseeingFromAPI = [];
    let sightseeingResponseMessage = "";

    let allFoodItemsForLocation = [];
    let foodResponseMessage = "";

    let allAccommodationOptions = [];
    let accommodationResponseMessage = "";

    let rawOutboundTransportOptions = null;
    let rawReturnTransportOptions = null;


    function getTimeValue(elementId) {
        const element = document.getElementById(elementId);
        return element && element.value ? element.value : null;
    }

    const foodSuggestionSelect = document.getElementById('foodSuggestion');
    const foodDetailsDiv = document.getElementById('foodDetails');
    if (foodSuggestionSelect && foodDetailsDiv) {
        foodSuggestionSelect.addEventListener('change', function () {
            foodDetailsDiv.style.display = this.value === 'Yes' ? 'block' : 'none';
        });
        foodDetailsDiv.style.display = foodSuggestionSelect.value === 'Yes' ? 'block' : 'none';
    }

    window.showOptions = function (direction) {
        const travelPrefElement = document.getElementById(`travelPreference${direction}`);
        const busOptionsElement = document.getElementById(`busOptions${direction}`);
        const trainOptionsElement = document.getElementById(`trainOptions${direction}`);
        if (travelPrefElement && busOptionsElement && trainOptionsElement) {
            const pref = travelPrefElement.value;
            busOptionsElement.style.display = pref === 'Bus' ? 'block' : 'none';
            trainOptionsElement.style.display = pref === 'Train' ? 'block' : 'none';
        }
    };
    showOptions('Onward');
    showOptions('Return');

    const accommodationPrefSelect = document.getElementById('accommodationPreference');
    const lowOptionsDiv = document.getElementById('lowOptions');
    if (accommodationPrefSelect && lowOptionsDiv) {
        accommodationPrefSelect.addEventListener('change', function () {
            lowOptionsDiv.style.display = this.value === 'Low' ? 'block' : 'none';
        });
        lowOptionsDiv.style.display = accommodationPrefSelect.value === 'Low' ? 'block' : 'none';
    }

    const travelForm = document.getElementById('travelForm');
    if (travelForm) {
        travelForm.addEventListener('submit', async function (event) {
            event.preventDefault();
            structuredPlans = []; numberOfPlans = 0; userSelectedTotalDays = 0;
            tripSource = ""; tripDestination = "";
            allSightseeingFromAPI = []; sightseeingResponseMessage = "";
            allFoodItemsForLocation = []; foodResponseMessage = "";
            allAccommodationOptions = []; accommodationResponseMessage = "";
            rawOutboundTransportOptions = null; rawReturnTransportOptions = null;

            const loadingOverlay = document.getElementById('loadingOverlay');
            if (loadingOverlay) loadingOverlay.style.display = 'flex';

            tripSource = document.getElementById('source').value;
            tripDestination = document.getElementById('destination').value;
            const daysValue = document.getElementById('days').value;
            userSelectedTotalDays = daysValue ? parseInt(daysValue) : 1;
            const budgetValue = document.getElementById('budget').value;

            const searchEntry = { source: tripSource, destination: tripDestination, days: userSelectedTotalDays, budget: parseInt(budgetValue) || 0, timestamp: new Date().toISOString() };
            try {
                let history = JSON.parse(localStorage.getItem('planningSearchHistory') || '[]');
                history.unshift(searchEntry); history = history.slice(0, 10);
                localStorage.setItem('planningSearchHistory', JSON.stringify(history));
            } catch (e) { console.error("Error saving search history:", e); }

            let cTravelPrf = document.getElementById('travelPreferenceOnward').value;
            let cBusType = null, cTrainCoach = null, cTravelStartTime = null, cTravelEndTime = null;
            if (cTravelPrf === 'Bus') { cBusType = document.getElementById('busTypeOnward').value || null; cTravelStartTime = getTimeValue('busStartTimeOnward'); cTravelEndTime = getTimeValue('busEndTimeOnward'); }
            else if (cTravelPrf === 'Train') { cTrainCoach = document.getElementById('trainCoachOnward').value || null; cTravelStartTime = getTimeValue('trainStartTimeOnward'); cTravelEndTime = getTimeValue('trainEndTimeOnward'); }
            else if (cTravelPrf === 'Any' || cTravelPrf === '') { cTravelPrf = "Bus"; }

            let cReturnTravelPrf = document.getElementById('travelPreferenceReturn').value;
            let cReturnBusType = null, cReturnTrainCoach = null, cReturnTravelStartTime = null, cReturnTravelEndTime = null;
            if (cReturnTravelPrf === 'Bus') { cReturnBusType = document.getElementById('busTypeReturn').value || null; cReturnTravelStartTime = getTimeValue('busStartTimeReturn'); cReturnTravelEndTime = getTimeValue('busEndTimeReturn'); }
            else if (cReturnTravelPrf === 'Train') { cReturnTrainCoach = document.getElementById('trainCoachReturn').value || null; cReturnTravelStartTime = getTimeValue('trainStartTimeReturn'); cReturnTravelEndTime = getTimeValue('trainEndTimeReturn'); }
            else if (cReturnTravelPrf === 'Any' || cReturnTravelPrf === '') { cReturnTravelPrf = "Bus"; }

            const accomPrefValue = document.getElementById('accommodationPreference').value;
            const foodSuggestionIsYes = document.getElementById('foodSuggestion').value === 'Yes';
            const foodChoiceValue = foodSuggestionIsYes ? (document.getElementById('foodChoice').value || null) : null;
            const formData = {
                cId: Date.now(), cName: "Travel User", cSrc: tripSource, cDes: tripDestination, cTotalDays: userSelectedTotalDays,
                cBudget: budgetValue ? parseInt(budgetValue) : null,
                cNsightseeing: document.getElementById('sightseeing').value ? parseInt(document.getElementById('sightseeing').value) : 0,
                cTravelPrf, cBusType, cTrainCoach, cTravelStartTime, cTravelEndTime,
                cReturnTravelPrf, cReturnBusType, cReturnTrainCoach, cReturnTravelStartTime, cReturnTravelEndTime,
                cAccomodationPrf: accomPrefValue || null,
                cLowType: accomPrefValue === 'Low' ? (document.getElementById('lowType').value || null) : null,
                cFoodSug: foodSuggestionIsYes, cFoodChoice: foodChoiceValue
            };

            try {
                const response = await fetch(`${API_BASE_URL}/clientPlanPreparing`, { method: "POST", headers: { "Content-Type": "application/json" }, body: JSON.stringify(formData) });
                const responseText = await response.text();
                console.log("Raw API Response Text:", responseText);

                if (!response.ok) {
                    let eDetail = responseText; try { eDetail = JSON.parse(responseText).detail || JSON.stringify(JSON.parse(responseText)); } catch (parseError) { console.warn("Could not parse error response as JSON:", parseError); }
                    throw new Error(`API error: ${response.status} - ${eDetail}`);
                }
                const result = JSON.parse(responseText);
                console.log("Parsed API Response (result):", result);

                const transportData = result[0];
                if (Array.isArray(transportData) && transportData.length > 0) {
                    rawOutboundTransportOptions = transportData[0];
                    if (transportData.length > 1) { rawReturnTransportOptions = transportData[1]; }
                    else { rawReturnTransportOptions = "No return transport details provided."; }
                } else { rawOutboundTransportOptions = "No transport details provided."; rawReturnTransportOptions = "No transport details provided."; }

                const sightseeingData = result[1];
                if (sightseeingData && typeof sightseeingData === 'object' && 'sight_seeing' in sightseeingData) {
                    allSightseeingFromAPI = sightseeingData.sight_seeing || [];
                    sightseeingResponseMessage = sightseeingData.message || (allSightseeingFromAPI.length === 0 ? "No sightseeing spots found." : "Sightseeing spots available.");
                } else { allSightseeingFromAPI = []; sightseeingResponseMessage = "Unexpected sightseeing data structure."; }

                const foodData = result[2];
                if (foodData && typeof foodData === 'object' && 'filtered_food' in foodData) {
                    allFoodItemsForLocation = foodData.filtered_food || [];
                    foodResponseMessage = foodData.message || (allFoodItemsForLocation.length === 0 ? "No food suggestions found." : "Food suggestions available.");
                } else { allFoodItemsForLocation = []; foodResponseMessage = "Unexpected food data structure."; }

                const accommodationData = result[3];
                if (accommodationData && typeof accommodationData === 'object' && 'accommodations' in accommodationData) {
                    allAccommodationOptions = accommodationData.accommodations || [];
                    accommodationResponseMessage = accommodationData.message || (allAccommodationOptions.length === 0 ? "No accommodation found." : "Accommodation options available.");
                } else if (Array.isArray(accommodationData)) {
                    allAccommodationOptions = accommodationData;
                    accommodationResponseMessage = accommodationData.length === 0 ? "No accommodation options found." : "Accommodation options available.";
                } else { allAccommodationOptions = []; accommodationResponseMessage = "Unexpected accommodation data structure."; }

                structureCombinedPlans();
                displayPlanButtons(numberOfPlans);
                if (numberOfPlans > 0) {
                    displaySinglePlanView(1);
                } else {
                    const displayArea = document.getElementById('dayPlanDisplay');
                    if(displayArea) displayArea.innerHTML = `<p class='no-data-message'>No complete travel plans could be generated based on available transport options. Please try different travel preferences.</p>`;
                }
                const resultOverlayDiv = document.getElementById('resultOverlay');
                if (resultOverlayDiv) resultOverlayDiv.style.display = 'flex';
            } catch (error) {
                console.error("Error in form submission or API processing:", error);
                const displayArea = document.getElementById('dayPlanDisplay');
                if (displayArea) displayArea.innerHTML = `<p class="error-message">An error occurred: ${error.message}. Check console.</p>`;
                const resultOverlay = document.getElementById('resultOverlay');
                if (resultOverlay) resultOverlay.style.display = 'flex';
                const planButtonsContainer = document.getElementById('dayButtonsContainer');
                if (planButtonsContainer) planButtonsContainer.innerHTML = '';
            } finally {
                if (loadingOverlay) loadingOverlay.style.display = 'none';
            }
        });
    }

    function structureCombinedPlans() {
        structuredPlans = [];
        numberOfPlans = 0;
        const outboundIsArray = Array.isArray(rawOutboundTransportOptions) && rawOutboundTransportOptions.length > 0;
        const returnIsArray = Array.isArray(rawReturnTransportOptions) && rawReturnTransportOptions.length > 0;

        if (outboundIsArray && returnIsArray) {
            numberOfPlans = Math.min(rawOutboundTransportOptions.length, rawReturnTransportOptions.length);
            for (let i = 0; i < numberOfPlans; i++) {
                structuredPlans.push({
                    planNumber: i + 1,
                    outboundTravel: rawOutboundTransportOptions[i],
                    returnTravel: rawReturnTransportOptions[i]
                });
            }
        } else if (outboundIsArray) {
           console.log("Only outbound transport options found. No complete round-trip plans generated based on pairs.");
        } else if (returnIsArray) {
            console.log("Only return transport options found. No complete round-trip plans generated based on pairs.");
        } else {
            console.log("Neither outbound nor return transport options are available in array format.");
        }
        if (typeof rawOutboundTransportOptions === 'string' || typeof rawReturnTransportOptions === 'string') {
            console.log("One or both transport options are messages, not arrays. No paired plans.");
            numberOfPlans = 0;
        }
    }

    function displayPlanButtons(numPlans) {
        const container = document.getElementById('dayButtonsContainer');
        if (!container) return;
        container.innerHTML = '';
        if (numPlans === 0) {
            container.innerHTML = "<p class='no-data-message'>No transport combinations found to create plans.</p>";
            return;
        }
        for (let i = 1; i <= numPlans; i++) {
            const button = document.createElement('button');
            button.classList.add('day-button');
            button.textContent = `Plan ${i}`;
            button.dataset.plan = i;
            button.addEventListener('click', function () {
                document.querySelectorAll('.day-button').forEach(btn => btn.classList.remove('active'));
                this.classList.add('active');
                
                const displayArea = document.getElementById('dayPlanDisplay');
                // Trigger fade out before changing content
                displayArea.classList.remove('visible');
                setTimeout(() => {
                    displaySinglePlanView(i);
                     // Trigger fade in after content is updated
                    displayArea.classList.add('visible');
                }, 300); // match this duration to a CSS transition if you have one
            });
            container.appendChild(button);
        }
        if (container.firstChild) {
            container.firstChild.classList.add('active');
        }
    }

    function displaySinglePlanView(planNumber) {
        const currentPlan = structuredPlans.find(p => p.planNumber === planNumber);
        const displayArea = document.getElementById('dayPlanDisplay');
        if (!displayArea) return;
        
        displayArea.innerHTML = '';
        displayArea.classList.remove('visible');

        if (!currentPlan && numberOfPlans > 0) {
            displayArea.innerHTML = `<p class='no-data-message'>No details available for this plan.</p>`;
            displayArea.classList.add('visible');
            return;
        }
        if (numberOfPlans === 0 && !currentPlan) {
            displayArea.innerHTML = `<p class='no-data-message'>Please generate a plan first or adjust travel preferences.</p>`;
            displayArea.classList.add('visible');
            return;
        }

        let html = `<div class="trip-header-card">
                        <h2>
                            <span class="location-highlight">${tripSource || 'N/A'}</span> 
                            <span class="arrow">➔</span> 
                            <span class="location-highlight">${tripDestination || 'N/A'}</span>
                        </h2>
                        <p>Displaying Plan ${planNumber} for your ${userSelectedTotalDays}-Day Trip</p>
                    </div>`;

        // --- TRANSPORTATION ---
        html += `<div class="itinerary-section-card">
                    <h4 class="section-title"><span class="icon">✈️</span> Transportation for Plan ${planNumber}</h4>`;
        
        html += `<h5 class="transport-direction-title">Outbound Journey</h5>`;
        if (currentPlan && currentPlan.outboundTravel) {
            const item = currentPlan.outboundTravel;
            if (typeof item === 'string') {
                html += `<div class="itinerary-item-card message-item"><p>${item}</p></div>`;
            } else {
                const transportIcon = item.Ttype === 'Bus' ? '🚌' : item.Ttype === 'Train' ? '🚆' : '➡️';
                html += `<div class="itinerary-item-card transport-item">
                             <div class="item-header">
                                 <span class="item-icon">${transportIcon}</span>
                                 <h5 class="item-name">${item.Tname || 'N/A'} (${item.Ttype || 'N/A'})</h5>
                             </div>
                             <div class="item-details-grid">
                                 <div class="detail-pair"><strong>Departs:</strong> <span>${item.Tdepa || 'N/A'}</span></div>
                                 <div class="detail-pair"><strong>Arrives:</strong> <span>${item.Tarr || 'N/A'}</span></div>
                                 <div class="detail-pair"><strong>Price:</strong> <span>${item.Tprice || 'N/A'}</span></div>
                                 <div class="detail-pair"><strong>Duration:</strong> <span>${item.Tdura || 'N/A'}</span></div>
                             </div>
                         </div>`;
            }
        } else { html += `<div class="itinerary-item-card"><p class='no-data-message'>No outbound transport details for this plan.</p></div>`; }

        html += `<h5 class="transport-direction-title">Return Journey</h5>`;
        if (currentPlan && currentPlan.returnTravel) {
            const item = currentPlan.returnTravel;
             if (typeof item === 'string') {
                html += `<div class="itinerary-item-card message-item"><p>${item}</p></div>`;
            } else {
                const transportIcon = item.Ttype === 'Bus' ? '🚌' : item.Ttype === 'Train' ? '🚆' : '➡️';
                html += `<div class="itinerary-item-card transport-item">
                             <div class="item-header">
                                 <span class="item-icon">${transportIcon}</span>
                                 <h5 class="item-name">${item.Tname || 'N/A'} (${item.Ttype || 'N/A'})</h5>
                             </div>
                             <div class="item-details-grid">
                                 <div class="detail-pair"><strong>Departs:</strong> <span>${item.Tdepa || 'N/A'}</span></div>
                                 <div class="detail-pair"><strong>Arrives:</strong> <span>${item.Tarr || 'N/A'}</span></div>
                                 <div class="detail-pair"><strong>Price:</strong> <span>${item.Tprice || 'N/A'}</span></div>
                                 <div class="detail-pair"><strong>Duration:</strong> <span>${item.Tdura || 'N/A'}</span></div>
                             </div>
                         </div>`;
            }
        } else { html += `<div class="itinerary-item-card"><p class='no-data-message'>No return transport details for this plan.</p></div>`; }
        html += `</div>`;


        // --- SIGHTSEEING ---
        html += `<div class="itinerary-section-card">
                    <h4 class="section-title"><span class="icon">🏞️</span> Sightseeing Spots in ${tripDestination}</h4>`;
        if (Array.isArray(allSightseeingFromAPI) && allSightseeingFromAPI.length > 0) {
            allSightseeingFromAPI.forEach(item => {
                let sightMapLink = '#';
                if (item.sLoc && item.sLoc.startsWith('http')) {
                    sightMapLink = item.sLoc;
                } else {
                    const sightQuery = `${item.sPlace || ''} ${item.sLoc || ''} ${tripDestination || ''}`.trim();
                    if (sightQuery) {
                         sightMapLink = `https://www.google.com/maps/search/?api=1&query=${encodeURIComponent(sightQuery)}`;
                    }
                }

                html += `<div class="itinerary-item-card sightseeing-item">
                            <div class="item-header">
                                <span class="item-icon">📸</span>
                                <h5 class="item-name">${item.sPlace || 'N/A'}</h5>
                            </div>
                            <div class="item-details-grid">
                                 <div class="detail-pair"><strong>Fee:</strong> <span>${item.sEnFee || 'N/A'}</span></div>
                                 <div class="detail-pair"><strong>Timings:</strong> <span>${item.sTimming || 'N/A'}</span></div>
                                 <div class="detail-pair"><strong>Best Time:</strong> <span>${item.sBestTime || 'N/A'}</span></div>
                            </div>
                            ${sightMapLink !== '#' ? `<a href="${sightMapLink}" target="_blank" class="maps-button"><span class="icon">📍</span> Open in Maps</a>` : ''}
                         </div>`;
            });
        } else {
            html += `<div class="itinerary-item-card message-item"><p class='no-data-message'>${sightseeingResponseMessage}</p></div>`;
        }
        html += `</div>`;

        // --- ACCOMMODATION ---
        html += `<div class="itinerary-section-card">
                    <h4 class="section-title"><span class="icon">🏨</span> Accommodation Options in ${tripDestination}</h4>`;
        if (Array.isArray(allAccommodationOptions) && allAccommodationOptions.length > 0) {
            allAccommodationOptions.forEach(item => {
                const fullAddressAcc = `${item.aName || ''}, ${item.aAdd || ''}, ${item.aLoc || ''}`;
                const mapLinkAcc = item.aLoc && item.aLoc.startsWith('http') ? item.aLoc : `https://www.google.com/maps/search/?api=1&query=${encodeURIComponent(fullAddressAcc)}`;
                html += `<div class="itinerary-item-card accommodation-item">
                            <div class="item-header">
                                <span class="item-icon">🏠</span>
                                <h5 class="item-name">${item.aName || 'N/A'}</h5>
                            </div>
                             <p class="item-subtitle">${item.aRoomtype || 'Type N/A'}</p>
                             <div class="item-details-grid">
                                 <div class="detail-pair"><strong>Price:</strong> <span>${typeof item.aPrice === 'number' ? '₹' + item.aPrice : (item.aPrice || 'N/A')}</span></div>
                                 <div class="detail-pair"><strong>Rating:</strong> <span class="rating">${item.aRating || 'N/A'} ${item.aRating ? '⭐' : ''}</span></div>
                                 <div class="detail-pair" style="grid-column: 1 / -1;"><strong>Address:</strong> <span>${item.aAdd || 'N/A'}</span></div>
                             </div>
                             <a href="${mapLinkAcc}" target="_blank" class="maps-button"><span class="icon">📍</span> Open in Maps</a>
                         </div>`;
            });
        } else {
            html += `<div class="itinerary-item-card message-item"><p class='no-data-message'>${accommodationResponseMessage}</p></div>`;
        }
        html += `</div>`;

        // --- FOOD ---
        html += `<div class="itinerary-section-card">
                    <h4 class="section-title"><span class="icon">🍲</span> Food Suggestions in ${tripDestination}</h4>`;
        if (Array.isArray(allFoodItemsForLocation) && allFoodItemsForLocation.length > 0) {
            allFoodItemsForLocation.forEach(item => {
                const mapLink = item.fLoc && item.fLoc.startsWith('http') ? item.fLoc : `https://www.google.com/maps/search/?api=1&query=${encodeURIComponent((item.fResname || '') + ', ' + (item.fAdd || ''))}`;
                html += `<div class="itinerary-item-card food-item">
                            <div class="item-header">
                                <span class="item-icon">🍽️</span>
                                <h5 class="item-name">${item.fItem || 'N/A'}</h5>
                            </div>
                            <p class="item-subtitle">at ${item.fResname || 'Restaurant N/A'} (${item.fAdd || 'Location N/A'})</p>
                            <a href="${mapLink}" target="_blank" class="maps-button"><span class="icon">📍</span> Open in Maps</a>
                         </div>`;
            });
        } else {
            html += `<div class="itinerary-item-card message-item"><p class='no-data-message'>${foodResponseMessage}</p></div>`;
        }
        html += `</div>`;

        displayArea.innerHTML = html;
        // Use a tiny timeout to allow the browser to render the new HTML before adding the class for the animation
        setTimeout(() => {
            displayArea.classList.add('visible');
        }, 10);
    }

    const closeResultBtn = document.getElementById('closeResultBtn');
    if (closeResultBtn) {
        closeResultBtn.addEventListener('click', function () {
            const resultOverlayDiv = document.getElementById('resultOverlay');
            if (resultOverlayDiv) resultOverlayDiv.style.display = 'none';
        });
    }

    const logoutBtn = document.getElementById("logoutBtn");
    if (logoutBtn) {
        logoutBtn.addEventListener("click", function (e) {
            e.preventDefault();
            alert('You have been logged out.');
            localStorage.removeItem("loggedInUser");
            window.location.href = "../Loginpage/login.html";
        });
    }
});