const wrapper = document.querySelector(".at-wrap");
const main = wrapper.querySelector(".at-main");

const settings = {
  display: {
    resources: {
      secondaryGlyphColor: '#0000',
    },
    staveProfile: 'tab',
    stretchForce: 0.5,
  },
  file: "{{ url_for('tabs.get_tab', tab_id=tab.id, file_id=tab.fileid) }}",
  notation: {
    elements: {
      ScoreTitle: false,
      ScoreSubTitle: false,
      ScoreArtist: false,
      ScoreAlbum: false,
      ScoreWords: false,
      ScoreMusic: false,
      ScoreWordsAndMusic: false,
      ScoreCopyright: false,
    },
    rhythmMode: 'showwithbars',
  },
  player: {
    enablePlayer: true,
    scrollElement: '.at-viewport',
    soundFont: '{{ url_for("static", filename="fonts/sonivox.sf2") }}',
  },
};
const api = new alphaTab.AlphaTabApi(main, settings);

const overlay = wrapper.querySelector(".at-overlay");
api.renderStarted.on(() => {
  overlay.style.display = 'flex';
});
api.renderFinished.on(() => {
  overlay.style.display = 'none';
});

function createTrackItem(track) {
  const trackItem = document
    .querySelector('#at-track-template')
    .content.cloneNode(true).firstElementChild;
  trackItem.querySelector('.at-track-name').innerText = track.name;
  trackItem.track = track;
  trackItem.onclick = (e) => {
    e.stopPropagation();
    api.renderTracks([track]);
  };
  return trackItem;
}

const trackList = document.querySelector('.at-track-list');
api.scoreLoaded.on((score) => {
  trackList.innerHTML = "";
  score.tracks.forEach((track) => {
    trackList.appendChild(createTrackItem(track));
  });
});

api.renderStarted.on(() => {
  const tracks = new Map();
  api.tracks.forEach((t) => {
    tracks.set(t.index, t);
  });

  const trackItems = trackList.querySelectorAll('.at-track');
  trackItems.forEach((trackItem) => {
    if (tracks.has(trackItem.track.index)) {
      trackItem.firstElementChild.classList.add('active');
    } else {
      trackItem.firstElementChild.classList.remove('active');
    }
  });
});

$('#at-print').click(function() {
  api.print();
});

$('#at-zoom ul button').click(function() {
  zoomValue = $(this).data('value');
  zoomLevel = parseInt(zoomValue) / 100;

  api.settings.display.scale = zoomLevel;
  api.updateSettings();
  api.render();

  $('#at-zoom ul button').removeClass('active');
});

$('#at-layout ul button').click(function() {
  value = $(this).data('value');

  switch (value) {
    case 'horizontal':
      api.settings.display.layoutMode = alphaTab.LayoutMode.Horizontal;
      break;
    case 'page':
      api.settings.display.layoutMode = alphaTab.LayoutMode.Page;
      break;
  }
  api.updateSettings();
  api.render();

  $('#at-layout ul button').removeClass('active');
});

const playerIndicator = wrapper.querySelector(
  '.at-controls .at-player-progress'
);
api.soundFontLoad.on((e) => {
  const percentage = Math.floor((e.loaded / e.total) * 100);
  playerIndicator.innerText = percentage + "%";
});
api.playerReady.on(()=>{
  playerIndicator.style.display = 'none';
});

const playPause = wrapper.querySelector(
  ".at-controls .at-player-play-pause"
);
const stop = wrapper.querySelector(".at-controls .at-player-stop");
playPause.onclick = (e) => {
  if (e.target.classList.contains("disabled")) {
    return;
  }
  api.playPause();
};
stop.onclick = (e) => {
  if (e.target.classList.contains("disabled")) {
    return;
  }
  api.stop();
};
api.playerReady.on(() => {
  playPause.classList.remove("disabled");
  stop.classList.remove("disabled");
});
api.playerStateChanged.on((e) => {
  const icon = playPause.querySelector("i.fas");
  if (e.state === alphaTab.synth.PlayerState.Playing) {
    icon.classList.remove("fa-play");
    icon.classList.add("fa-pause");
  } else {
    icon.classList.remove("fa-pause");
    icon.classList.add("fa-play");
  }
});

var tracklistSetup = false;
api.renderFinished.on(() => {
  // set zoom level visual
  zoomValue = parseInt(api.settings.display.scale * 100);
  $("#at-zoom ul button[data-value='" + zoomValue + "']").addClass('active');

  // set layout mode visual
  layoutMode = api.settings.display.layoutMode
  layoutStr = ''
  switch (layoutMode) {
    case alphaTab.LayoutMode.Horizontal:
      layoutStr = 'horizontal';
      break;
    case alphaTab.LayoutMode.Page:
      layoutStr = 'page';
      break;
  }
  $("#at-layout ul button[data-value='" + layoutStr + "']").addClass('active');

  // set up track list
  if (!tracklistSetup) {
    tracks = api.score.tracks;
    for (i = 0; i < tracks.length; i++) {
      var html = `<div class="d-flex flex-wrap align-items-center mt-1">
        <div class="me-3" style="width: 6rem;"><em>${tracks[i].name}</em></div>
        <div class="me-1"><i class="fa fa-volume-up"></i></div>
        <input type="range" class="form-range track-volume flex-fill" data-trackid="${i}" min="0" max="1.2" step="0.1" value="1" style="width: auto;">
        <div class="ms-3 btn-group" role="group">
          <button data-trackid="${i}" class="solo-button btn btn-outline-warning btn-sm">S</button>
          <button data-trackid="${i}" class="mute-button btn btn-outline-danger btn-sm">M</button>
        </div>
      </div>`;
      $('#ps-track-list').append(html);
    }

    $('.solo-button').click(function() {
      trackNo = $(this).data('trackid');
      track = api.score.tracks[trackNo];
      soloState = $(this).hasClass('btn-outline-warning');

      $(this).toggleClass('btn-outline-warning');
      $(this).toggleClass('btn-warning');

      api.changeTrackSolo([track], soloState);
    });

    $('.mute-button').click(function() {
      trackNo = $(this).data('trackid');
      track = api.score.tracks[trackNo];
      soloState = $(this).hasClass('btn-outline-danger');

      $(this).toggleClass('btn-outline-danger');
      $(this).toggleClass('btn-danger');

      api.changeTrackMute([track], soloState);
    });

    $('.track-volume').click(function() {
      trackNo = $(this).data('trackid');
      track = api.score.tracks[trackNo];

      api.changeTrackVolume([track], $(this).val());
    });

    tracklistSetup = true;
  }
});

function formatDuration(milliseconds) {
  let seconds = milliseconds / 1000;
  const minutes = (seconds / 60) | 0;
  seconds = (seconds - minutes * 60) | 0;
  return (
    String(minutes).padStart(2, "0") +
    ":" +
    String(seconds).padStart(2, "0")
  );
}

const songPosition = wrapper.querySelector(".at-song-position");
let previousTime = -1;
api.playerPositionChanged.on((e) => {
  // reduce number of UI updates to second changes.
  const currentSeconds = (e.currentTime / 1000) | 0;
  if (currentSeconds == previousTime) {
    return;
  }

  songPosition.innerText =
    formatDuration(e.currentTime) + " / " + formatDuration(e.endTime);
});

// settings modal
$('#ps-metronome').change(function() {
  if (this.checked) {
    api.metronomeVolume = 1;
  } else {
    api.metronomeVolume = 0;
  }
});

$('#ps-loop').change(function() {
  if (this.checked) {
    api.isLooping = true;
  } else {
    api.isLooping = false;
  }
});

$('#ps-speed').change(function() {
  speed = parseInt($(this).val());
  api.playbackSpeed = speed / 100;
  $('#ps-custom-speed').val(speed);
});

$('#ps-custom-speed').change(function() {
  speed = parseInt($(this).val());
  api.playbackSpeed = speed / 100;
  $('#ps-speed').val(speed);
});

$('#ps-transpose').change(function() {
  transpose = parseInt($(this).val());
  api.settings.notation.transpositionPitches = [transpose];
});
