import { Cw3FrontendPage } from './app.po';

describe('cw3-frontend App', () => {
  let page: Cw3FrontendPage;

  beforeEach(() => {
    page = new Cw3FrontendPage();
  });

  it('should display welcome message', () => {
    page.navigateTo();
    expect(page.getParagraphText()).toEqual('Welcome to app!!');
  });
});
