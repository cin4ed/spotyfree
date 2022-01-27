<script>
    export let isHidden = true;
</script>

<span class="popup" class:hidden={isHidden}><p>invalid url 🤯</p></span>

<style>
    .popup {
        position: absolute;
        top: 380%;
        left: 0%;

        z-index: 1;

        width: fit-content;
        padding: 0.5em 1em;
        border-radius: 5px;

        background: linear-gradient(
            45deg,
            rgba(245, 177, 97, 1),
            rgba(236, 54, 110, 1) 80%
        ) !important;

        font-family: "Varela Round", sans-serif;
        color: white;
        font-size: 1rem;
        white-space: nowrap;

        transition: transform 250ms ease-in-out;
    }

    .popup::after {
        content: "";
        
        position: absolute;
        top: -21%;
        left: 50%;
        transform: rotateZ(180deg);

        margin-left: -5px;
        border-width: 5px;
        border-style: solid;
        border-color: rgba(232, 114, 105, 1) transparent transparent transparent;
    }

    .hidden {
        transform: scale(0);
    }
</style>
