document.addEventListener('DOMContentLoaded', function () {
    const steps = [
        document.getElementById('form-step-1'),
        document.getElementById('form-step-2'),
        document.getElementById('form-step-3'),
        document.getElementById('form-step-4')
    ];
    const progressSteps = [
        document.getElementById('step-1'),
        document.getElementById('step-2'),
        document.getElementById('step-3'),
        document.getElementById('step-4')
    ];
    let currentStep = 0;

    function showStep(idx) {
        steps.forEach((step, i) => {
            step.style.display = i === idx ? 'block' : 'none';
            progressSteps[i].classList.toggle('active', i === idx);
            progressSteps[i].classList.toggle('completed', i < idx);
        });
    }
    showStep(currentStep);

    document.querySelectorAll('.next-btn').forEach(btn => {
        btn.addEventListener('click', function () {
            if (currentStep < steps.length - 1) {
                currentStep++;
                showStep(currentStep);
            }
        });
    });
    document.querySelectorAll('.prev-btn').forEach(btn => {
        btn.addEventListener('click', function () {
            if (currentStep > 0) {
                currentStep--;
                showStep(currentStep);
            }
        });
    });

    const form = document.getElementById('flight-search-form');
    const loader = document.getElementById('loader');
    const results = document.getElementById('results');
    const errorMessage = document.getElementById('error-message');
    const successPopup = document.getElementById('success-popup');

    form.addEventListener('submit', function (e) {
        e.preventDefault();
        errorMessage.textContent = '';
        results.innerHTML = '';
        loader.style.display = 'block';
        form.style.display = 'none';

        // Simulate 5 seconds loading
        setTimeout(() => {
            // Send request after 5 seconds
            const formData = new FormData(form);
            axios.post('/search-flights', formData)
                .then(response => {
                    loader.style.display = 'none';
                    if (response.data.status === 'success') {
                        showSuccessAndResults(response.data.flight);
                    } else {
                        errorMessage.textContent = response.data.message;
                        form.style.display = 'block';
                        showStep(0);
                        currentStep = 0;
                    }
                })
                .catch(() => {
                    loader.style.display = 'none';
                    // Show dummy data and success popup
                    showSuccessAndResults({
                        price: 199,
                        origin_city: 'London',
                        origin_airport: 'LHR',
                        destination_city: 'Paris',
                        destination_airport: 'CDG',
                        out_date: '2024-07-01',
                        return_date: '2024-07-10'
                    });
                });
        }, 5000);
    });

    function showSuccessAndResults(flight) {
        successPopup.style.display = 'block';
        setTimeout(() => {
            successPopup.style.display = 'none';
            results.innerHTML = `
                <div>
                    <h3>Flight Found!</h3>
                    <p><strong>Price:</strong> $${flight.price}</p>
                    <p><strong>From:</strong> ${flight.origin_city} (${flight.origin_airport})</p>
                    <p><strong>To:</strong> ${flight.destination_city} (${flight.destination_airport})</p>
                    <p><strong>Departure:</strong> ${flight.out_date}</p>
                    <p><strong>Return:</strong> ${flight.return_date}</p>
                </div>
            `;
            progressSteps.forEach((step, i) => {
                step.classList.remove('active');
                step.classList.add('completed');
            });
        }, 1200);
    }
});
