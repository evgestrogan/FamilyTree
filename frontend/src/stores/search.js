import { ref } from "vue";
import { defineStore } from "pinia";

export const useSearchStore = defineStore("search", () => {
  const searchRequest = ref("");
  const selfPeople = ref([
    {
      id: 1,
      name: "Ivanov Ivan Ivanovich",
      date: "12.12.1978-17.06.2003",
    },
    {
      id: 2,
      name: "Vasilev Anatoliy Genadievich",
      date: "12.12.1978-17.06.2003",
    },
    {
      id: 3,
      name: "Klarson Kent Anatolievich",
      date: "12.12.1978-17.06.2003",
    },
    {
      id: 4,
      name: "Slimus Ruslan Andreevich",
      date: "12.12.1978-17.06.2003",
    },
  ]);
  const globalPeople = ref([
    {
      name: "Asmaa O'Brien Ivanovich",
      date: "12.12.1978-17.06.2003",
    },
    {
      name: "Isla-Mae Kaye Genadievich",
      date: "12.12.1978-17.06.2003",
    },
    {
      name: "Jaydon Little Anatolievich",
      date: "12.12.1978-17.06.2003",
    },
    {
      name: "Barbara Walters Andreevich",
      date: "12.12.1978-17.06.2003",
    },
    {
      name: "Brent Keller Genaf",
      date: "12.12.1978-17.06.2003",
    },
  ]);
  const searchGraph = ref(true);
  const searchSelf = ref(true);
  const searchGlobal = ref(true);

  function setSearchRequest(request) {
    searchRequest.value = request;
  }

  function setSearchGraph(status) {
    searchGraph.value = status;
  }

  function setSearchSelf(status) {
    searchSelf.value = status;
  }

  function setSearchGlobal(status) {
    searchGlobal.value = status;
  }

  return {
    searchRequest,
    selfPeople,
    globalPeople,
    searchGraph,
    searchSelf,
    searchGlobal,
    setSearchRequest,
    setSearchGraph,
    setSearchSelf,
    setSearchGlobal,
  };
});
