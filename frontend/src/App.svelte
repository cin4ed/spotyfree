<script>
	// components
	import Searcher from "./Searcher.svelte"
	import TrackCard from "./TrackCard.svelte"
	import Popup from "./Popup.svelte";
	import downloadjs from "downloadjs";
	import { Wave } from 'svelte-loading-spinners'

	// transitions
	import { scale } from 'svelte/transition'

	// class triggers
	let welcomePosition = true

	// state handlers
	let isUrlValid = true
	let invalidUrlInterm = false
	let isPopupHidden = true
	let showLoadingAnimation = false
	let opacityTranTimer = 500 // change in transition propert

	// logic
	const url = 'MyUrl'
	let showingTracks = []

	// <SearchHandling>
		function handleInvalidUrl() {
			// <Digusting ugly motherfucker animation handling, but it works>
				isPopupHidden = false
				invalidUrlInterm = true
				setTimeout(() => {
					isUrlValid = false
					invalidUrlInterm= false
				}, opacityTranTimer) // transition opacity time

				setTimeout(() => {
					invalidUrlInterm= true
					setTimeout(() => {
						isUrlValid = true
						invalidUrlInterm = false
						isPopupHidden = true
					}, opacityTranTimer); // transition opacity time
				}, opacityTranTimer*2) // transition opacity time *2
			// </Digusting ugly motherfucker animation handling, but it works>
		}


		function bufferizeTracks(tracks) {
			/*
				tl;dr bufferizeTracks allows to show one by one animation on TrackCards

				it sets an timer of 150ms to add tracks to showingTracks and allow them
				to be displayed with an animation one by one and not all of them at the same 
				time, I'm shure this is not the ideal method but works.
			*/
			const timer = 150

			showingTracks = []
			let interval = setInterval(function() {
				if (tracks.length > 0) {
					// if not empty: shift the first element from tracks and add them to
					// showing tracks 
					let track = tracks.shift()
					showingTracks = [...showingTracks, track]
				} else clearInterval(interval) // if tracks empty: delete the interval
			}, timer)
		}


		// when a search is performed this function is called
		function handleSearch(e) {
			showLoadingAnimation = true

			// get the search query from the event
			const query = e.target[0].value

			// talk with the api and handle server response
			fetch(`${url}/search?q=${query}`)
				.then((response) => response.json())
				.then((data) => {
					showLoadingAnimation = false

					// if query is not valid
					if (!data.status.valid_query) {
						handleInvalidUrl()
						return
					}

					// if query is valid
					welcomePosition = false
					bufferizeTracks(data.resource)
				})
		}
	// </SearchHandling>



	function handleSongDownload(e) {
		// get the song url
		const songUrl = e.detail.url

		// handle what happen with the track card when download
		e.detail.showLoading()

		// talk with the api to perform the download
		fetch(`${url}/download?q=${songUrl}`)
			.then((response) => response.blob())
			.then((blob) => {

				// donwload the file response
				downloadjs(blob, e.detail.songName)
				e.detail.disable()
			})
	}
</script>

<div class="app" >
	<div class="header-wrapper" class:welcome-position={welcomePosition}>
		<div class="header">
			<h1 class="header__title">
				<span class="header__span-1">Spoty</span><span class="header__span-2" class:invalid-url={!isUrlValid} class:valid-url={isUrlValid} class:invalid-url-interm={invalidUrlInterm}>free</span>
				<Popup isHidde />
			</h1>
		</div>

		<div class="main">
			<Searcher on:submit={handleSearch} />
		</div>

		{#if showLoadingAnimation}
			<div class="loading-container">
				<Wave size="60" color="#91f5b7" unit="px" duration="1s"></Wave>
			</div>
		{/if}
	</div>

	<div class="tracks">
		{#each showingTracks as track (track)}
			<div in:scale class='test'>
				<TrackCard {track} on:download={handleSongDownload} />
			</div>
		{/each}
	</div>
</div>

<style>
	.app {
		grid-area: content;
		min-height: 100vh;
	}

	.header-wrapper {
		transition: all 400ms ease-in-out;
	}

	.header {
		text-align: center;
		margin: 1em;
	}

	.header h1 {
		display: inline;
		position: relative;
	}

	.header__span-1 {
		font-family: "PT Sans Narrow", sans-serif;
	}

	.header__span-2 {
		font-family: "Satisfy", cursive;
		font-size: 1.2em;
		padding: 4px;
		transition: opacity 500ms ease-in-out
	}

	.invalid-url-interm {
		opacity: 0;
	}

	.invalid-url {
		background: linear-gradient(45deg, #93F9B9, #1D976C 80%);
		background-clip: text;
		-webkit-background-clip: text;
		-webkit-text-fill-color: transparent;	
	}

	.invalid-url {  /* invalid url trigging */
		background: linear-gradient(45deg, rgba(245,177,97,1), rgba(236,54,110,1) 80%) !important;
		background-clip: text !important;
		-webkit-background-clip: text !important;
		-webkit-text-fill-color: transparent !important;
	}	

	.welcome-position {
		transform: translateY(32vh);
	}

	.loading-container {
		width: fit-content;
		margin: 3em auto 0 auto;
	}

	@media screen and (min-width: 320px) { /* 320px — 480px: Mobile devices */
		.app {
			padding: 10px 25px;
			font-size: 14px;
		}
	}
</style>
