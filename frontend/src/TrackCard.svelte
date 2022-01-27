<script>
    import { Circle } from 'svelte-loading-spinners'
    import { createEventDispatcher } from 'svelte'
    export let track

    let downloading = false
    let dissapear = false
    let hide = false

    const dispatch = createEventDispatcher()
    const dispatchDownload = () => {
        dispatch('download', { 
            url: track.external_urls.spotify, 
            songName: track.name, 
            showLoading: () => { downloading = true },
            disable: () => { 
                // first opactity 0 then after 2 seg visibility hidden
                dissapear = true
                setTimeout(() => {hide = true}, 500)
            }
        })
    }
</script>

<div class="track-card" class:dissapear={dissapear} class:hide={hide}>
    <img class="track-card__photo" src="{track.album.images[1].url || ""}" alt="song cover ">
    <div class="track-card__description">
        <p class="track-card__song-name">{track.name}</p>
        <p class="track-card__song-album">{track.album.name}</p>
    </div>
    {#if !downloading }
    <button on:click={dispatchDownload} class="track-card__download-btn">
        <svg class="track-card__download-svg" version="1.1" id="Layer_1" xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" x="0px" y="0px" viewBox="0 0 330 330" style="enable-background:new 0 0 330 330;" xml:space="preserve">
            <g id="XMLID_23_">
                <path id="XMLID_24_" d="M154.389,255.602c0.351,0.351,0.719,0.683,1.103,0.998c0.169,0.138,0.347,0.258,0.52,0.388c0.218,0.164,0.432,0.333,0.659,0.484c0.212,0.142,0.432,0.265,0.649,0.395c0.202,0.121,0.4,0.248,0.608,0.359c0.223,0.12,0.453,0.221,0.681,0.328c0.215,0.102,0.427,0.21,0.648,0.301c0.223,0.092,0.45,0.167,0.676,0.247c0.236,0.085,0.468,0.175,0.709,0.248c0.226,0.068,0.456,0.119,0.684,0.176c0.246,0.062,0.489,0.131,0.739,0.181c0.263,0.052,0.529,0.083,0.794,0.121c0.219,0.031,0.435,0.073,0.658,0.095c0.492,0.048,0.986,0.075,1.48,0.075c0.494,0,0.988-0.026,1.479-0.075c0.226-0.022,0.444-0.064,0.667-0.096c0.262-0.037,0.524-0.068,0.784-0.12c0.255-0.05,0.504-0.121,0.754-0.184c0.223-0.057,0.448-0.105,0.669-0.172c0.246-0.075,0.483-0.167,0.724-0.253c0.221-0.08,0.444-0.152,0.662-0.242c0.225-0.093,0.44-0.202,0.659-0.306c0.225-0.106,0.452-0.206,0.672-0.324c0.21-0.112,0.408-0.239,0.611-0.361c0.217-0.13,0.437-0.252,0.648-0.394c0.222-0.148,0.431-0.314,0.644-0.473c0.179-0.134,0.362-0.258,0.536-0.4c0.365-0.3,0.714-0.617,1.049-0.949c0.016-0.016,0.034-0.028,0.049-0.044l70.002-69.998c5.858-5.858,5.858-15.355,0-21.213c-5.857-5.857-15.355-5.858-21.213-0.001l-44.396,44.393V25c0-8.284-6.716-15-15-15c-8.284,0-15,6.716-15,15v183.785l-44.392-44.391c-5.857-5.858-15.355-5.858-21.213,0c-5.858,5.858-5.858,15.355,0,21.213L154.389,255.602z"/>
                <path id="XMLID_25_" d="M315,160c-8.284,0-15,6.716-15,15v115H30V175c0-8.284-6.716-15-15-15c-8.284,0-15,6.716-15,15v130c0,8.284,6.716,15,15,15h300c8.284,0,15-6.716,15-15V175C330,166.716,323.284,160,315,160z"/>
            </g>
        </svg>
    </button>
    {:else}
        <div class="track-card__loading">
            <Circle size="40" color="#FFF" unit="px" duration="1s"></Circle>
        </div>
    {/if}
</div>

<style>
    .track-card {
        color: #FFF;
        font-family: 'Rubik', sans-serif;

        transition: all ease-in-out, 
                    opacity 500ms, 
                    transform 500ms;

        margin: 1.4em 0;

        overflow: hidden;
        border-radius: 12px;

        box-shadow: rgba(100, 100, 111, 0.2) 0px 7px 29px 0px;

        background: linear-gradient(to left, rgb(31 36 108), rgb(32 203 151));

        display: grid;
        grid-template-columns: 80px minmax(170px, 1fr) min-content;
        grid-template-areas: "photo description download";
    }

    .track-card__photo {
        max-width: 80px;
        max-height: 80px;

        grid-area: photo;
    }

    .track-card__description {
        padding: 1em;

        display: flex;
        flex-direction: column;
        justify-content: center;

        white-space: nowrap;
        overflow: hidden;

        grid-area: description;
    }

    .track-card__song-name {
        font-weight: 500;
        overflow: hidden;
    }

    .track-card__song-album {
        font-weight: 300;
        overflow: hidden;
    }

    .track-card__download-btn {
        width: 50px;
        margin-right: 13px;
        margin: 0 13px 0px 0;

        border: none;
        outline: none;

        background: none;

        grid-area: download;

        position: relative;

        z-index: 1;
    }

    .track-card__download-btn::before {
        content: "";

        position: absolute;
        top: 0px;
        left: -53px;

        width: 40px;
        height: 80px;
        z-index: 1000;

        box-shadow: -40px 0px 30px -49px #1211112e inset;
    }

    .track-card__download-svg {
        fill: white;
        stroke-width: 1px;
    }

    .track-card__loading {
        display: flex;
        align-items: center;
        margin: 0 13px 0px 0;
        width: 50px;
    }

    .dissapear {
        transform: scale(.2);
        opacity: 0;
    }

    .hide {
        display: none;
    }

</style>