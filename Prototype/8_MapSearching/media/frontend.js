// Handle search form submission
      document
        .getElementById("searchForm")
        .addEventListener("submit", function (event) {
          event.preventDefault(); // Prevent the default form submission
          const query = document.getElementById("searchInput").value;
          fetchAndUpdateGraph("/search", { query: query });
        });