export default async function loadQuestions(programId, questionType,token) {
    const options = {
        method: 'GET',
        mode: 'cors',
        headers: {
            'Accept': 'application/json',
            'Content-Type': 'application/json',
            'Authorization': 'Token ' + token,
        },
    }
    let input = 'http://localhost:8000/api/program/' + programId + '/question-' + questionType + '/?format=json';
    let response = await fetch(input, options);
    return await response.json();
}
