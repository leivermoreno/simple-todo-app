document.querySelectorAll(".btn-danger").forEach(function(el) {
    el.addEventListener("click", function(e) {
        let answer = confirm("Are you sure?");
        if (!answer)
        {
            e.preventDefault()
        }
    });
});