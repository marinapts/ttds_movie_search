(this.webpackJsonpgui=this.webpackJsonpgui||[]).push([[0],{100:function(e,a,t){},102:function(e,a,t){},107:function(e,a,t){},109:function(e,a,t){},110:function(e,a,t){},111:function(e,a,t){},130:function(e,a,t){},131:function(e,a,t){},132:function(e,a,t){"use strict";t.r(a);var n=t(0),r=t.n(n),c=t(11),o=t.n(c),i=(t(100),t(38)),s=t.n(i),l=t(13),m=t(12),u=t(15),h=t(16),d=t(17),v=t(171),p=t(172),f=t(43),y=t(164),g=t(54),E=t(10),b=t(81),w=t(160),C=t(173),S=t(53),k=t(161),j=t(175),O=t(162),N=t(83),M=t(163),T=t(155),I=t(76),x=t.n(I),q=t(78),A=t.n(q),D=t(79),B=t.n(D),Y=t(77),_=t.n(Y),G=(t(102),function(e){function a(e){var t;return Object(l.a)(this,a),(t=Object(u.a)(this,Object(h.a)(a).call(this,e))).onHandleYearChange=function(e,a){return t.setState(Object(E.a)({},e,a))},t.onHandleChange=function(e,a){"year"===e&&(a="".concat(t.state.fromYear,"-").concat(t.state.toYear)),t.props.onAdvancedSearchChange(e,a)},t.state={fromYear:"",toYear:"",year:""},t}return Object(d.a)(a,e),Object(m.a)(a,[{key:"render",value:function(){var e=this,a=this.state,t=a.fromYear,n=a.toYear,c=this.props,o=c.enableAdvancedSearch,i=c.data;return r.a.createElement(T.a,{in:o},r.a.createElement("div",{className:"adv-search"},r.a.createElement("div",{className:"adv-search-container"},r.a.createElement(w.a,{container:!0,spacing:1,alignItems:"space-between",className:"adv-search-item"},r.a.createElement(x.a,{className:"adv-search-icon",color:"primary"}),r.a.createElement(C.a,{className:"adv-search-input",value:i.movieTitle,label:"Movie title",onChange:function(a){return e.onHandleChange("movieTitle",a.target.value)}})),r.a.createElement(w.a,{container:!0,spacing:1,alignItems:"space-between",className:"adv-search-item"},r.a.createElement(_.a,{className:"adv-search-icon",color:"primary"}),r.a.createElement(C.a,{className:"adv-search-input",value:i.actor,label:"Actor/Actress",onChange:function(a){return e.onHandleChange("actor",a.target.value)}}))),r.a.createElement("div",{className:"adv-search-container"},r.a.createElement(w.a,{container:!0,spacing:1,alignItems:"space-between",className:"adv-search-item"},r.a.createElement(A.a,{className:"adv-search-icon",color:"primary"}),r.a.createElement("div",{className:"year"},r.a.createElement(C.a,{className:"adv-search-input year-input",value:t,label:"From year",onChange:function(a){return e.onHandleYearChange("fromYear",a.target.value)},onBlur:function(a){return setTimeout((function(){return e.onHandleChange("year",e.state.year)}),.5)}}),r.a.createElement(C.a,{className:"adv-search-input year-input",value:n,label:"To year",onChange:function(a){return e.onHandleYearChange("toYear",a.target.value)},onBlur:function(a){return e.onHandleChange("year",e.state.year)}}))),r.a.createElement(w.a,{container:!0,spacing:1,alignItems:"space-between",className:"adv-search-item"},r.a.createElement(B.a,{className:"adv-search-icon",color:"primary"}),r.a.createElement(C.a,{className:"adv-search-input",value:i.keywords,label:"Keywords",onChange:function(a){return e.onHandleChange("keywords",a.target.value)}})))))}}]),a}(n.Component)),H=(t(107),function(e){function a(e){var t;return Object(l.a)(this,a),(t=Object(u.a)(this,Object(h.a)(a).call(this,e))).onSearchChange=function(e){t.setState({query:e.target.value})},t.setSearchInput=function(e){t.setState({query:e.target.text},t.selectSearch)},t.toggleAdvancedSearch=function(){return t.setState({enableAdvancedSearch:!t.state.enableAdvancedSearch})},t.onAdvancedSearchChange=function(e,a){var n,r="";if("year"===e){var c=a.split("-"),o=Object(b.a)(c,2),i=o[0],s=o[1];i=parseInt(i),s=parseInt(s),i.length&&isNaN(i)||s.length&&isNaN(s)?r="Year should be a number in the range 1900-2020":i&&s?(a="".concat(i,"-").concat(s),(i>s||i<1900||s>2020)&&(r="Invalid year range")):i||s?!i&&s?a="1900-".concat(s):i&&!s&&(a="".concat(i,"-2020")):a=""}t.setState((n={},Object(E.a)(n,e,a),Object(E.a)(n,"invalidMessage",r),n))},t.selectSearch=function(e){e&&e.preventDefault();var a=t.state,n=a.query,r={movieTitle:a.movieTitle,actor:a.actor,year:a.year,keywords:a.keywords};t.props.performSearch(Object(g.a)({query:n},r),t.state.movieSearchEnabled)},t.toggleMovieSearch=function(e){var a=t.state,n=a.query,r=a.movieTitle,c=a.actor,o=a.year,i=a.keywords,s=e.target.checked;t.setState({movieSearchEnabled:s},(function(){if(n.length){var e={movieTitle:r,actor:c,year:o,keywords:i};t.props.performSearch(Object(g.a)({query:n},e),s)}}))},t.state={query:"",movieTitle:"",actor:"",year:"",fromYear:"",toYear:"",keywords:"",enableAdvancedSearch:!1,movieSearchEnabled:!1,invalidMessage:""},t}return Object(d.a)(a,e),Object(m.a)(a,[{key:"componentDidMount",value:function(){this.setState({showErrorMsg:!1,invalidMessage:""})}},{key:"render",value:function(){var e=this.state,a=e.enableAdvancedSearch,t=e.movieTitle,n=e.actor,c=e.year,o=e.keywords,i=e.movieSearchEnabled,s=e.invalidMessage,l=this.props,m=l.showErrorMsg,u=l.showExamples,h={movieTitle:t,actor:n,year:c,keywords:o};return r.a.createElement(w.a,{item:!0,xs:12},r.a.createElement("form",{noValidate:!0,autoComplete:"off",onSubmit:this.selectSearch},r.a.createElement("div",{className:"search-form"},r.a.createElement("div",{className:"search-input"},r.a.createElement(C.a,{id:"outlined-basic",label:"Search for a movie quote...",variant:"outlined",fullWidth:!0,onChange:this.onSearchChange,value:this.state.query})),r.a.createElement(S.a,{className:"search-button",variant:"outlined",color:"primary",type:"submit"},"Search"),r.a.createElement(k.a,{className:"movie-search",control:r.a.createElement(j.a,{checked:i,onChange:this.toggleMovieSearch,color:"primary",inputProps:{"aria-label":"primary checkbox"}}),label:"Search for movies"})),r.a.createElement(k.a,{className:"advanced-search-button",color:"primary",control:r.a.createElement(O.a,{checked:a,onChange:this.toggleAdvancedSearch,value:"checkedB",color:"primary"}),label:"Advanced Search"}),r.a.createElement(G,{enableAdvancedSearch:a,data:h,onAdvancedSearchChange:this.onAdvancedSearchChange}),s.length?r.a.createElement(N.a,{variant:"body1",className:"error-message"},s):""),u&&r.a.createElement(N.a,{variant:"h6",color:"primary",className:"examples"},r.a.createElement("span",null,"Try ",r.a.createElement(M.a,{color:"primary",underline:"none",variant:"inherit",onClick:this.setSearchInput},"Carpe Diem")),r.a.createElement("span",null," or ",r.a.createElement(M.a,{color:"primary",underline:"none",variant:"inherit",onClick:this.setSearchInput},"Following's not really my style"))),m&&r.a.createElement("h6",{className:"error-container"},"Error: API not running. Go to ttds_movie_search/api and run ./run.sh"))}}]),a}(n.Component)),P=t(170),V=t(55),F=t.n(V),W=t(165),J=t(166),K=t(167),Q=t(168),R=(t(109),function(e){function a(){var e,t;Object(l.a)(this,a);for(var n=arguments.length,r=new Array(n),c=0;c<n;c++)r[c]=arguments[c];return(t=Object(u.a)(this,(e=Object(h.a)(a)).call.apply(e,[this].concat(r)))).viewDetails=function(){t.props.viewDetails(t.props.movie_id)},t.convertMsToTime=function(e){parseInt(e%1e3/100);var a=Math.floor(e/1e3%60),t=Math.floor(e/6e4%60),n=Math.floor(e/36e5%24);return t=t<10?"0"+t:t,a=a<10?"0"+a:a,"".concat(n=n<10?"0"+n:n,":").concat(t,":").concat(a)},t}return Object(d.a)(a,e),Object(m.a)(a,[{key:"render",value:function(){var e=this.props,a=e.full_quote,t=e.title,n=e.character_name,c=e.categories,o=e.time_ms,i=(e.plotKeywords,a&&a.length>200?"".concat(a.substr(0,200),"..."):a);return r.a.createElement("div",null,r.a.createElement(W.a,{raised:!0,className:"card-container"},r.a.createElement(J.a,{className:"card-media",image:this.props.thumbnail}),r.a.createElement(K.a,{onClick:this.viewDetails},r.a.createElement("div",{className:"card-content"},r.a.createElement(Q.a,null,r.a.createElement(N.a,{variant:"h5"},i),r.a.createElement(N.a,{variant:"h6"},t),r.a.createElement("br",null),r.a.createElement(N.a,{variant:"body2"},"Character: ",n),r.a.createElement(N.a,{variant:"body2"},"Category: ",c.join(", ")),r.a.createElement(N.a,{variant:"body2"},"Quote was said at ",this.convertMsToTime(o)))))))}}]),a}(r.a.Component)),U=(t(110),function(e){function a(e){var t;return Object(l.a)(this,a),(t=Object(u.a)(this,Object(h.a)(a).call(this,e))).showMoreCast=function(e){e.preventDefault(),t.setState({moreCastVisible:!t.state.moreCastVisible})},t.state={moreCastVisible:!1},t}return Object(d.a)(a,e),Object(m.a)(a,[{key:"componentDidUpdate",value:function(e){e.details._id!==this.props.details._id&&this.setState({moreCastVisible:!1})}},{key:"render",value:function(){var e=this.props,a=e.details,t=e.errorMovieInfoMsg,c=this.state.moreCastVisible,o=0;return a.cast&&(o=a.cast.length>10?10:a.cast.length),r.a.createElement("div",Object.assign({},this.props,{className:"details-card"}),r.a.createElement(W.a,{raised:!0,className:"card-container"},r.a.createElement(Q.a,null,r.a.createElement("div",{className:"card-content"},t.length?r.a.createElement(Q.a,null,r.a.createElement(N.a,{variant:"h6",color:"secondary"},t)):a&&r.a.createElement(Q.a,null,r.a.createElement(N.a,{variant:"h5"},a.title),r.a.createElement(N.a,{variant:"body1"},a.description),r.a.createElement(N.a,{variant:"body1"},r.a.createElement("b",null,"Year:")," ",a.year),r.a.createElement(N.a,{variant:"body1",gutterBottom:!0},r.a.createElement("b",null,"Rating:")," ",a.rating),o>0&&a.cast.length>0&&r.a.createElement(N.a,{variant:"h5"},"Cast"),o>0&&a.cast.slice(0,o).map((function(e){return r.a.createElement(N.a,{key:e.actor,variant:"body1"},e.actor," as ",r.a.createElement("i",null,e.character))})),o>0&&a.cast.length>10&&r.a.createElement(n.Fragment,null,!c&&r.a.createElement(M.a,{onClick:this.showMoreCast},r.a.createElement(N.a,null,"Show more...")),c&&a.cast.slice(10,-1).map((function(e){return r.a.createElement(N.a,{key:e.actor,variant:"body1"},e.actor," as ",r.a.createElement("i",null,e.character))}))),r.a.createElement("br",null),r.a.createElement(N.a,{variant:"body1",gutterBottom:!0}),r.a.createElement(S.a,{target:"_blank",variant:"contained",color:"primary",href:"https://www.imdb.com/title/".concat(a._id)},"View in IMDB"))))))}}]),a}(n.Component)),L=t(169),$=(t(111),function(e){function a(e){var t;return Object(l.a)(this,a),(t=Object(u.a)(this,Object(h.a)(a).call(this,e))).filterByGenre=function(e){var a=t.state.variants,n=Object.keys(a).filter((function(e){return"contained"===a[e]}));for(var r in a)r in n||(a[r]="text");n.includes(e)||(a[e]="contained"),t.setState({variants:a},(function(){return t.props.filterByGenre(a)}))},t.state={variants:{},selectedGenres:[]},t}return Object(d.a)(a,e),Object(m.a)(a,[{key:"componentWillMount",value:function(){var e={};this.props.genres.forEach((function(a){e[a]="text"})),this.setState({variants:e})}},{key:"render",value:function(){var e=this,a=this.props.genres;return r.a.createElement(L.a,{color:"primary","aria-label":"primary button group",className:"genre-filtering"},a.map((function(a,t){return r.a.createElement(z,{key:a,genre:a,variant:e.state.variants[a],filterByGenre:e.filterByGenre})})))}}]),a}(n.Component)),z=function(e){function a(){var e,t;Object(l.a)(this,a);for(var n=arguments.length,r=new Array(n),c=0;c<n;c++)r[c]=arguments[c];return(t=Object(u.a)(this,(e=Object(h.a)(a)).call.apply(e,[this].concat(r)))).onGenreClick=function(e){t.props.filterByGenre(e)},t}return Object(d.a)(a,e),Object(m.a)(a,[{key:"render",value:function(){var e=this,a=this.props,t=a.genre,n=a.variant;return r.a.createElement(S.a,{variant:n,color:"primary",id:t,onClick:function(){return e.onGenreClick(t)}},t)}}]),a}(n.Component),X=t(80),Z=t.n(X).a.create({baseURL:"http://167.71.139.222/",responseType:"json"}),ee=(t(130),function(e){function a(e){var t;return Object(l.a)(this,a),(t=Object(u.a)(this,Object(h.a)(a).call(this,e))).filterByGenre=function(e){var a=t.props.data,n=Object.keys(e).filter((function(a){return"contained"===e[a]}));n.length&&(a=a.filter((function(e){return e.categories.includes(n[0])}))),t.setState({data:a,showDetails:!1,offset:0})},t.viewMovieInfoCard=function(e){var a,n,r;return s.a.async((function(c){for(;;)switch(c.prev=c.next){case 0:return a="",n={},c.prev=2,c.next=5,s.a.awrap(Z.get("/movie/".concat(e)));case 5:r=c.sent,n=r.data,c.next=13;break;case 9:c.prev=9,c.t0=c.catch(2),a="Movie not found",n={};case 13:t.setState({showDetails:!0,movieInfo:n,errorMovieInfoMsg:a});case 14:case"end":return c.stop()}}),null,null,[[2,9]])},t.handleClick=function(e){t.setState({offset:e})},t.state={data:[],showDetails:!1,quoteId:null,offset:0,perPage:10,errorMovieInfoMsg:"",movieInfo:{}},t}return Object(d.a)(a,e),Object(m.a)(a,[{key:"componentDidMount",value:function(){this.setState({data:this.props.data,showDetails:!1})}},{key:"render",value:function(){var e=this,a=this.state,t=a.showDetails,n=a.data,c=a.offset,o=a.perPage,i=a.movieInfo,s=a.errorMovieInfoMsg,l=this.props,m=l.genres,u=l.queryTime,h=(Math.round(100*u)/100).toFixed(3);return r.a.createElement("div",null,r.a.createElement(w.a,{container:!0,className:"movies-container",spacing:6},n.length>0&&r.a.createElement(w.a,{item:!0,xs:12},r.a.createElement($,{genres:m,filterByGenre:this.filterByGenre})),r.a.createElement(w.a,{item:!0,xs:8},r.a.createElement(N.a,{variant:"body1",className:"query-results"},"Query results: ".concat(n.length," movies (").concat(h," seconds)")),n.length>o&&r.a.createElement(F.a,{limit:o,offset:c,total:n.length,currentPageColor:"primary",onClick:function(a,t){return e.handleClick(t)}}),n.slice(c,c+o).map((function(a,t){return r.a.createElement(R,Object.assign({key:t,viewDetails:e.viewMovieInfoCard},a))})),n.length>o&&r.a.createElement(F.a,{limit:o,offset:c,total:n.length,currentPageColor:"primary",onClick:function(a,t){return e.handleClick(t)}})),t&&r.a.createElement(w.a,{item:!0,xs:4},r.a.createElement(P.a,{in:t,style:{transitionDelay:t?"100ms":"0ms"}},r.a.createElement(U,{details:i,errorMovieInfoMsg:s})))))}}]),a}(r.a.Component)),ae=(t(131),Object(f.a)({palette:{type:"dark",primary:{main:"#2196f3"},secondary:{light:"#cc33ff",main:"#e699ff",contrastText:"#ffcc00"}}})),te=function(e){function a(e){var t;return Object(l.a)(this,a),(t=Object(u.a)(this,Object(h.a)(a).call(this,e))).performSearch=function(e,a){var n=e.query,r=e.movieTitle,c=e.actor,o=e.year,i=e.keywords;t.setState({loading:!0},(function(){var e;return s.a.async((function(l){for(;;)switch(l.prev=l.next){case 0:return l.prev=0,l.next=3,s.a.awrap(Z.post(a?"/movie_search":"/query_search",{query:n,movie_title:r,actor:c,year:o,keywords:i}));case 3:e=l.sent,t.setState({movies:e.data.movies,genres:e.data.category_list,queryTime:e.data.query_time,showCards:!0,showExamples:!1,loading:!1}),l.next=11;break;case 7:l.prev=7,l.t0=l.catch(0),console.error(l.t0),t.setState({showErrorMsg:!0,showExamples:!0,loading:!1});case 11:case"end":return l.stop()}}),null,null,[[0,7]])}))},t.state={movies:[],showCards:!1,showExamples:!0,showErrorMsg:!1,loading:!1,queryTime:0},t}return Object(d.a)(a,e),Object(m.a)(a,[{key:"render",value:function(){var e=this.state,a=e.showCards,t=e.movies,c=e.genres,o=e.showExamples,i=e.showErrorMsg,s=e.loading,l=e.queryTime;return r.a.createElement(y.a,{theme:ae},r.a.createElement(v.a,{className:"app"},r.a.createElement("h3",null,"TTDS Movie Project 2020"),r.a.createElement("div",{className:"search-container"},r.a.createElement(H,{performSearch:this.performSearch,showExamples:o,showErrorMsg:i})),r.a.createElement(n.Fragment,null,s?r.a.createElement(n.Fragment,null,Array.apply(null,{length:3}).map((function(e,a){return r.a.createElement(p.a,{variant:"rect",width:790,height:170,className:"skeleton-card"})}))):a&&r.a.createElement(ee,{data:t,genres:c,queryTime:l}))))}}]),a}(n.Component);Boolean("localhost"===window.location.hostname||"[::1]"===window.location.hostname||window.location.hostname.match(/^127(?:\.(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)){3}$/));o.a.render(r.a.createElement(te,null),document.getElementById("root")),"serviceWorker"in navigator&&navigator.serviceWorker.ready.then((function(e){e.unregister()}))},95:function(e,a,t){e.exports=t(132)}},[[95,1,2]]]);
//# sourceMappingURL=main.95f3b8df.chunk.js.map