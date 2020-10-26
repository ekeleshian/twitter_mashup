const dropdownleft = document.getElementById("dropdown1");
const dropdownright = document.getElementById("dropdown2");
const submitBtn = document.getElementById('submitBtn');

let leftUser;
let rightUser;
dropdownleft.addEventListener("change", (event) => {
  leftUser = event.target.value;

});

dropdownright.addEventListener("change", (event) => {
  rightUser = event.target.value;
});


submitBtn.addEventListener("click", (event) => {
  const sortedUsers = [leftUser, rightUser];

  sortedUsers.sort(function (a, b) {
    if (a.toLowerCase() < b.toLowerCase()) {
      return -1;
    } else if (a.toLowerCase() > b.toLowerCase()) {
      return 1;
    } else {
      return 0;
    }
  });

  fetch(`http://127.0.0.1:5000/submit/${sortedUsers[0]}/${sortedUsers[1]}`)
      .then(function (response) {
        return response.json();
      })
      .then(function (data) {
        console.log({data})
      })
      .catch(function(e) {
    console.log({e})
  })
});

