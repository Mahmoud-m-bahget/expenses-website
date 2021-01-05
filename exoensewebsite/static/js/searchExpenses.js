const searchField = document.querySelector('#searchField');
const tableOutput = document.querySelector('.table-output')
const appTable = document.querySelector('.app-table')
const paginationContainer = document.querySelector('.pagination-container')
const tbody = document.querySelector('.table-body')
const noResult = document.querySelector('.no-result')
tableOutput.style.display = 'none'
tbody.innerHTML=""
noResult.style.display = 'none'


searchField.addEventListener('keyup',(e)=>{
    const searchValue = e.target.value;
    noResult.style.display = 'none'

    if (searchValue.trim().length > 0) {
        noResult.style.display = 'none'
        paginationContainer.style.display='none';
        tbody.innerHTML="";
        fetch("/search-expenses",{
            body: JSON.stringify({searchText:searchValue}),
            method: "POST",
        })
        .then((res)=>res.json())
        .then((data)=>{
            console.log(data);
            tableOutput.style.display = 'block';
            appTable.style.display='none';

           if (data.length===0){
            tableOutput.style.display = 'none';
            noResult.style.display = 'block'

           }else{
                noResult.style.display = 'none'

            data.forEach( (item) => {
                tbody.innerHTML += `
                <tr>
                <td>${item.amount}</td>
                <td>${item.category}</td>
                <td>${item.description}</td>
                <td>${item.date}</td>
                </tr>
                `
               });
           }
        });
    }else{
        appTable.style.display='block';
        paginationContainer.style.display='block';
        tableOutput.style.display = "none";
    }
});