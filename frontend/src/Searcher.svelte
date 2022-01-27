<script>
    let placeholder = 'your link here'
</script>

<form on:submit|preventDefault>
    <div class="searcher">
        <span class="searcher__link-emoji">🔗</span>
        <input class="searcher__input" type="text" placeholder={placeholder}>
        <input type="submit" class="searcher__button" value="🔎">
    </div>
</form>

<style>
    .searcher {
        border-radius: 25px; 
        overflow: hidden;       

        display: grid;
        grid-template-columns: auto 1fr auto;
        grid-template-rows: 50px;

        box-shadow: rgba(17, 12, 46, 0.15) 0px 48px 100px 0px;

        background: linear-gradient(to left, #93F9B9, #25c28b); 
        background: #b4e5d9;
    }

    .searcher__link-emoji {
        padding: 10px 15px;

        background: none;

        display: flex;
        align-items: center;
    }

    .searcher__input {
        padding-left: 4px;
        padding-right: 4px;

        border: none;
        background-color: white;

        font-size: 1rem;
        
        opacity: 100% !important;

        text-align: center;

    }

    .searcher__input::placeholder {
        font-family: 'Ubuntu Mono', monospace;
    }

    .searcher__input:focus {
        outline: none;
    }

    .searcher__button {
        padding: 5px 15px;
        border: none;

        color: white;
        font-size: 20px;

        background:none;
    }

    .searcher__button:active {
        transform: scale(1.2);
    }

    input:focus, textarea:focus, select:focus{
        outline: none;
    }
</style>