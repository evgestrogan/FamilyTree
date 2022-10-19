const WorkSpace = () => import("../views/WorkSpace.vue");
const Tree = () => import("../components/Tree/Tree.vue");
const TreeSideBar = () => import("../components/Tree/TreeSideBar.vue");
const DropDownTreeSearch = () =>
  import("../components/Tree/Search/DropDownTreeSearch.vue");
const ModalTreeSearch = () =>
  import("../components/Tree/Search/ModalTreeSearch.vue");
const Chat = () => import("../components/Chat/Chat.vue");
const ChatSideBar = () => import("../components/Chat/ChatSideBar.vue");
const Profile = () => import("../components/Profile/Profile.vue");
const ProfileSideBar = () => import("../components/Profile/ProfileSideBar.vue");

export default {
  path: "/",
  redirect: { name: "Tree" },
  component: WorkSpace,
  children: [
    {
      path: "/profile",
      name: "Profile",
      components: {
        default: Profile,
        sidebar: ProfileSideBar,
      },
      meta: {
        isAuth: true,
      },
    },
    {
      path: "/chat",
      name: "Chat",
      components: {
        default: Chat,
        sidebar: ChatSideBar,
      },
      meta: {
        isAuth: true,
      },
    },
    {
      path: "/tree",
      name: "Tree",
      components: {
        default: Tree,
        sidebar: TreeSideBar,
        navContent: DropDownTreeSearch,
      },
      meta: {
        isAuth: true,
      },
      children: [
        {
          path: "/tree/search/:variant",
          name: "Search",
          component: ModalTreeSearch,
          meta: {
            isAuth: true,
          },
        },
      ],
    },
  ],
};
