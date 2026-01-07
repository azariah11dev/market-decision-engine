document.addEventListener("DOMContentLoaded", () => {
    const initial_amount = document.getElementById("container-1-initial-amount");
    const stock_ticker = document.getElementById("container-1-stock-ticker");
    const initial_date = document.getElementById("container-1-initial-date");
    const final_date = document.getElementById("container-1-final-date");
    const interval = document.getElementById("container-1-interval");
    const benchmark = document.getElementById("container-1-options-benchmark");
    const sector = document.getElementById("container-1-options-sector");
    const analyze = document.getElementById("container-1-analyze-btn");

    analyze.addEventListener("click", async () => {
        const amount_value = parseFloat(initial_amount.value);
        const ticker_value = stock_ticker.value.trim();
        const initial_date_value = initial_date.value;
        const final_date_value = final_date.value;
        const interval_value = interval.value;
        const benchmark_value = benchmark.value;
        const sector_value = sector.value;

        if (isNaN(amount_value) ||
            ticker_value === "" ||
            initial_date_value === "" ||
            final_date_value === ""
        ) {
            alert("The fields in customize data cannot be empty");
        }
        else {
            try {
                const ticker_response = await fetch(`http://localhost:8000/quotes/${ticker_value}?start_date=${initial_date_value}&end_date=${final_date_value}&interval=${interval_value}`, {
                    method: "POST",
                    mode: "cors",
                    headers: { "Content-Type": "application/json" },
                    body: JSON.stringify({ starting_balance: amount_value,
                        ticker: ticker_value,
                        start_date: initial_date_value,
                        end_date: final_date_value,
                        interval: interval_value,
                        sector: sector_value
                     })
                });

                const ticker_data = await ticker_response.json();
                console.log(ticker_data);
            } catch (error) {
            console.error(error);
            }
        }

        if (benchmark_value === "") {
            console.log(benchmark_value);
        }
        else {
            try {
                const benchmark_response = await fetch(`http://localhost:8000/quotes/${benchmark_value}?start_date=${initial_date_value}&end_date=${final_date_value}&interval=${interval_value}`, {
                    method: "POST",
                    mode: "cors",
                    headers: { "Content-Type": "application/json" },
                    body: JSON.stringify({ starting_balance: amount_value,
                        ticker: benchmark_value,
                        start_date: initial_date_value,
                        end_date: final_date_value,
                        interval: interval_value,
                     })
                });

                const benchmark_data = await benchmark_response.json();
                console.log(benchmark_data);
            } catch (error) {
                console.error(error);
            }
        }

        if (sector_value === "") {
            console.log(sector_value);
        }
        else {
            try {
                const sector_response = await fetch(`http://localhost:8000/quotes/${sector_value}?start_date=${initial_date_value}&end_date=${final_date_value}&interval=${interval_value}`, {
                    method: "POST",
                    mode: "cors",
                    headers: { "Content-Type": "application/json" },
                    body: JSON.stringify({ starting_balance: amount_value,
                        ticker: sector_value,
                        start_date: initial_date_value,
                        start_date: initial_date_value,
                        end_date: final_date_value,
                        interval: interval_value
                     })
                });

                const sector_data = await sector_response.json();
                console.log(sector_data)
            } catch (error) {
                console.error(error);
            }
        }
    
    });
});